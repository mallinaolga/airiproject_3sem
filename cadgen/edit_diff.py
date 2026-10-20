"""
Построчное сравнение двух текстов.

- **unified diff**: :func:`git_unified_diff`, применение — :func:`apply_unified_diff` / :func:`parse_unified_diff`.
- Структурный разбор: :func:`line_edits`; пары «до/после»: :func:`line_replace_pairs` / :func:`apply_line_replace_pairs`.
- Последовательные замены по уникальному ``old_string``: :func:`replace_edits` / :func:`apply_replace_edits`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher, unified_diff
from enum import Enum


class EditKind(str, Enum):
    EQUAL = "equal"
    DELETE = "delete"
    INSERT = "insert"
    REPLACE = "replace"


@dataclass(frozen=True)
class LineEdit:
    """Диапазоны строк [start, end) как у ``difflib.SequenceMatcher.get_opcodes``."""

    kind: EditKind
    s1_start: int
    s1_end: int
    s2_start: int
    s2_end: int

    def lines_removed(self, lines_s1: list[str]) -> list[str]:
        if self.kind not in (EditKind.DELETE, EditKind.REPLACE):
            return []
        return lines_s1[self.s1_start : self.s1_end]

    def lines_added(self, lines_s2: list[str]) -> list[str]:
        if self.kind not in (EditKind.INSERT, EditKind.REPLACE):
            return []
        return lines_s2[self.s2_start : self.s2_end]


def split_lines(s: str) -> list[str]:
    return s.splitlines()


def git_unified_diff(
    s1: str,
    s2: str,
    *,
    context_lines: int = 3,
) -> str:
    """
    Unified diff (формат ``difflib.unified_diff``, совместимый с ``patch``).

    Имена файлов не подставляются — только hunks ``@@`` и строки ``-``/``+``/пробел.

    Строки через ``splitlines()``; каждая строка патча с ``\\n``.
    """
    lines1 = split_lines(s1)
    lines2 = split_lines(s2)
    # difflib только для заголовков добавляет lineterm; строки hunk (+/-/пробел) — без \n,
    # из-за чего "".join склеивает их в одну линию. Нормализуем: каждая строка патча с \n.
    parts: list[str] = []
    for chunk in unified_diff(
        lines1,
        lines2,
        fromfile="",
        tofile="",
        n=context_lines,
        lineterm="",
    ):
        parts.append(chunk if chunk.endswith("\n") else chunk + "\n")
    return "".join(parts)


_HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


@dataclass(frozen=True)
class UnifiedHunk:
    """Один hunk unified diff: ``old_start`` (1-based в старом файле) и строки `` `` / ``-`` / ``+``."""

    old_start: int
    lines: list[tuple[str, str]]  # (' '|'-'|'+', текст без префикса)


def parse_unified_diff(patch: str) -> list[UnifiedHunk]:
    """
    Разобрать unified diff (как у :func:`difflib.unified_diff` / :func:`git_unified_diff`).
    Игнорирует ``diff --git``, ``---``, ``+++``, строки ``\\ No newline...``.
    """
    raw = patch.splitlines()
    i = 0
    hunks: list[UnifiedHunk] = []
    while i < len(raw):
        line = raw[i]
        if line.startswith("diff --git"):
            i += 1
            continue
        if line.startswith("---"):
            i += 1
            if i < len(raw) and raw[i].startswith("+++"):
                i += 1
            continue
        if line.startswith("@@"):
            m = _HUNK_HEADER.match(line)
            if not m:
                raise ValueError(f"invalid hunk header: {line!r}")
            old_start = int(m.group(1))
            i += 1
            body: list[tuple[str, str]] = []
            while i < len(raw):
                ln = raw[i]
                if ln.startswith("@@") or ln.startswith("---"):
                    break
                if ln.startswith("\\"):
                    i += 1
                    continue
                if not ln:
                    raise ValueError("blank line inside hunk")
                prefix = ln[0]
                if prefix not in " -+":
                    raise ValueError(f"unexpected line in hunk: {ln!r}")
                body.append((prefix, ln[1:]))
                i += 1
            hunks.append(UnifiedHunk(old_start=old_start, lines=body))
            continue
        i += 1
    return hunks


def apply_unified_diff(original: str, patch: str) -> str:
    """
    Применить unified diff к строке ``original`` (построчно, как после ``splitlines``).

    Контекст и удаления проверяются на совпадение; при расхождении — ``ValueError``.
    Совместимо с патчем из :func:`git_unified_diff`.
    """
    orig_lines = split_lines(original)
    hunks = parse_unified_diff(patch)
    out: list[str] = []
    orig_pos = 0

    for hunk in hunks:
        if hunk.old_start == 0:
            insert_at = 0
        else:
            insert_at = hunk.old_start - 1
        if insert_at < orig_pos:
            raise ValueError(
                f"hunks overlap or wrong order: expected orig_pos <= {insert_at}, got {orig_pos}"
            )
        out.extend(orig_lines[orig_pos:insert_at])
        orig_pos = insert_at

        for prefix, text in hunk.lines:
            if prefix == " ":
                if orig_pos >= len(orig_lines) or orig_lines[orig_pos] != text:
                    got = orig_lines[orig_pos] if orig_pos < len(orig_lines) else "<eof>"
                    raise ValueError(
                        f"context mismatch at old line {orig_pos + 1}: "
                        f"expected {text!r}, got {got!r}"
                    )
                out.append(text)
                orig_pos += 1
            elif prefix == "-":
                if orig_pos >= len(orig_lines) or orig_lines[orig_pos] != text:
                    got = orig_lines[orig_pos] if orig_pos < len(orig_lines) else "<eof>"
                    raise ValueError(
                        f"delete mismatch at old line {orig_pos + 1}: "
                        f"expected {text!r}, got {got!r}"
                    )
                orig_pos += 1
            else:
                out.append(text)

    out.extend(orig_lines[orig_pos:])
    return join_lines(out)


def line_edits(s1: str, s2: str, *, autojunk: bool = False) -> tuple[list[str], list[str], list[LineEdit]]:
    """
    Возвращает ``(lines1, lines2, edits)``.

    Каждый ``LineEdit`` — один блок opcodes по строкам:
    *equal*, *delete*, *insert*, *replace*.
    """
    lines1 = split_lines(s1)
    lines2 = split_lines(s2)
    matcher = SequenceMatcher(None, lines1, lines2, autojunk=autojunk)
    edits = [
        LineEdit(EditKind(tag), i1, i2, j1, j2)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
    ]
    return lines1, lines2, edits


def line_edits_changes_only(s1: str, s2: str, *, autojunk: bool = False) -> list[LineEdit]:
    """Только шаги, где нужно что-то менять (без *equal*)."""
    _, _, ops = line_edits(s1, s2, autojunk=autojunk)
    return [op for op in ops if op.kind != EditKind.EQUAL]


def line_replace_pairs(
    s1: str,
    s2: str,
    *,
    autojunk: bool = False,
    include_equal: bool = True,
) -> list[tuple[str, str]]:
    """
    Список пар «до / после» по строкам в порядке ``SequenceMatcher.get_opcodes``.

    * *equal* (если ``include_equal``): ``(блок, тот же блок)`` — блок из ``s1``, ``\\n`` между строками.
    * *delete*: ``(удаляемый блок, пустая строка)``.
    * *insert*: ``(пустая строка, вставляемый блок)`` — вставка в текущую позицию (между уже обработанным
      префиксом ``original`` и ещё не прочитанным хвостом).
    * *replace*: ``(старый блок, новый блок)``.

    Для :func:`apply_line_replace_pairs` нужны пары с ``include_equal=True`` (по умолчанию),
    полученные с тем же ``s1``, что подаётся в ``apply``.
    При ``include_equal=False`` список короче (удобно для LLM), но такой список **нельзя**
    надёжно применить без полного плана.
    """
    lines1, lines2, edits = line_edits(s1, s2, autojunk=autojunk)
    pairs: list[tuple[str, str]] = []
    for op in edits:
        if op.kind == EditKind.EQUAL:
            if not include_equal:
                continue
            blk = join_lines(lines1[op.s1_start : op.s1_end])
            pairs.append((blk, blk))
        elif op.kind == EditKind.DELETE:
            blk = join_lines(lines1[op.s1_start : op.s1_end])
            pairs.append((blk, ""))
        elif op.kind == EditKind.INSERT:
            blk = join_lines(lines2[op.s2_start : op.s2_end])
            pairs.append(("", blk))
        else:
            old_b = join_lines(lines1[op.s1_start : op.s1_end])
            new_b = join_lines(lines2[op.s2_start : op.s2_end])
            pairs.append((old_b, new_b))
    return pairs


def apply_line_replace_pairs(original: str, pairs: list[tuple[str, str]]) -> str:
    """
    Применить к ``original`` пары из :func:`line_replace_pairs` с ``include_equal=True``.

    Обходит ``original`` слева направло: вставки не сдвигают указатель в ``original``,
    остальные шаги читают и проверяют следующие строки ``original``.
    В конце весь текст должен быть исчерпан.
    """
    lines = split_lines(original)
    i = 0
    out: list[str] = []
    for before, after in pairs:
        if before == "":
            out.extend(split_lines(after))
            continue
        if after == "":
            b = split_lines(before)
            n = len(b)
            if lines[i : i + n] != b:
                raise ValueError(
                    f"delete mismatch at line {i + 1}: expected {b!r}, got {lines[i : i + n]!r}"
                )
            i += n
            continue
        if before == after:
            b = split_lines(before)
            n = len(b)
            if lines[i : i + n] != b:
                raise ValueError(
                    f"equal mismatch at line {i + 1}: expected {b!r}, got {lines[i : i + n]!r}"
                )
            out.extend(b)
            i += n
            continue
        b = split_lines(before)
        n = len(b)
        if lines[i : i + n] != b:
            raise ValueError(
                f"replace mismatch at line {i + 1}: expected {b!r}, got {lines[i : i + n]!r}"
            )
        out.extend(split_lines(after))
        i += n

    if i != len(lines):
        raise ValueError(f"not all original lines consumed: remaining from line {i + 1}: {lines[i:]!r}")
    return join_lines(out)


def join_lines(lines: list[str]) -> str:
    """Склеить строки так же, как обычно сравнивают текст без финального ``\\n``."""
    return "\n".join(lines)


def _ensure_single_occurrence(cur: str, old: str) -> None:
    if old == "":
        return
    n = cur.count(old)
    if n != 1:
        raise ValueError(f"old_string must occur exactly once in document, got {n}: {old!r}")


def replace_edits(before: str, after: str, *, autojunk: bool = False) -> list[tuple[str, str]]:
    """
    Две версии текста → список последовательных замен ``[(old_string, new_string), ...]``.

    На каждом шаге ``old_string`` встречается в **текущем** тексте ровно один раз (при генерации
    контекст расширяется вверх по строкам). Применение — :func:`apply_replace_edits`
    (первое вхождение за шаг).

    Параметр ``autojunk`` зарезервирован под единый API с :func:`line_edits`; алгоритм сводит
    ``cur`` к ``after`` итеративно по строкам.
    """
    del autojunk
    edits: list[tuple[str, str]] = []
    cur = before
    target = after
    while cur != target:
        cl = split_lines(cur)
        tl = split_lines(target)
        i = 0
        while i < len(cl) and i < len(tl) and cl[i] == tl[i]:
            i += 1
        j = 0
        while (
            j < len(cl) - i
            and j < len(tl) - i
            and cl[len(cl) - 1 - j] == tl[len(tl) - 1 - j]
        ):
            j += 1
        end_cl = len(cl) - j
        end_tl = len(tl) - j
        old_mid = join_lines(cl[i:end_cl])
        new_mid = join_lines(tl[i:end_tl])

        if old_mid == "":
            if cur == "":
                edits.append(("", new_mid))
                cur = new_mid
                continue
            if i == len(cl):
                anchor = cl[-1]
                pair = (anchor, anchor + "\n" + new_mid)
            elif i == 0:
                anchor = cl[0]
                pair = (anchor, new_mid + "\n" + anchor)
            else:
                pair = (
                    cl[i - 1] + "\n" + cl[i],
                    cl[i - 1] + "\n" + new_mid + "\n" + cl[i],
                )
            _ensure_single_occurrence(cur, pair[0])
            edits.append(pair)
            cur = cur.replace(pair[0], pair[1], 1)
            continue

        lo = i
        while True:
            old_str = join_lines(cl[lo:end_cl])
            new_str = join_lines(tl[lo:end_tl])
            if cur.count(old_str) == 1:
                edits.append((old_str, new_str))
                cur = cur.replace(old_str, new_str, 1)
                break
            if lo == 0:
                raise ValueError(
                    f"cannot build unique old_string for replace step near line {i + 1}: {old_mid!r}"
                )
            lo -= 1
    return edits


def apply_replace_edits(original: str, edits: list[tuple[str, str]], *, unique: bool = True) -> str:
    """
    Применить последовательность пар ``old_string`` / ``new_string``: на каждом шаге подставляется
    **первое** вхождение ``old_string``.

    При ``unique=True`` для непустого ``old_string`` требуется ровно одно вхождение в текущем тексте.
    Пустой ``old_string``: одна вставка в начало (как при ``str.replace`` с пустым искомым и лимитом 1).
    """
    cur = original
    for old_s, new_s in edits:
        if unique and old_s != "":
            _ensure_single_occurrence(cur, old_s)
        if old_s == "":
            cur = cur.replace("", new_s, 1)
        else:
            cur = cur.replace(old_s, new_s, 1)
    return cur


def reconstruct_s2(lines1: list[str], lines2: list[str], edits: list[LineEdit]) -> str:
    """Проверка: результат должен совпасть с ``join_lines(lines2)``."""
    out: list[str] = []
    for op in edits:
        if op.kind == EditKind.EQUAL:
            out.extend(lines1[op.s1_start : op.s1_end])
        elif op.kind == EditKind.DELETE:
            continue
        elif op.kind == EditKind.INSERT:
            out.extend(lines2[op.s2_start : op.s2_end])
        elif op.kind == EditKind.REPLACE:
            out.extend(lines2[op.s2_start : op.s2_end])
    return join_lines(out)


def format_line_plan(
    s1: str,
    s2: str,
    *,
    include_equal: bool = False,
    autojunk: bool = False,
    one_based: bool = True,
) -> str:
    """Краткое текстовое описание операций (номера строк — 1-based если ``one_based``)."""

    def ln(i: int) -> int:
        return i + 1 if one_based else i

    lines1, lines2, edits = line_edits(s1, s2, autojunk=autojunk)
    parts: list[str] = []
    for op in edits:
        if op.kind == EditKind.EQUAL and not include_equal:
            continue
        if op.kind == EditKind.EQUAL:
            parts.append(
                f"keep s1 lines [{ln(op.s1_start)}:{ln(op.s1_end)}) "
                f"== s2 [{ln(op.s2_start)}:{ln(op.s2_end)})"
            )
        elif op.kind == EditKind.DELETE:
            parts.append(
                f"delete s1 lines [{ln(op.s1_start)}:{ln(op.s1_end)}): "
                + repr(lines1[op.s1_start : op.s1_end])
            )
        elif op.kind == EditKind.INSERT:
            parts.append(
                f"insert before s1 line {ln(op.s1_start)} from s2 "
                f"[{ln(op.s2_start)}:{ln(op.s2_end)}): "
                + repr(lines2[op.s2_start : op.s2_end])
            )
        else:
            parts.append(
                f"replace s1 [{ln(op.s1_start)}:{ln(op.s1_end)}) -> "
                f"s2 [{ln(op.s2_start)}:{ln(op.s2_end)}):\n"
                f"  - {repr(lines1[op.s1_start : op.s1_end])}\n"
                f"  + {repr(lines2[op.s2_start : op.s2_end])}"
            )
    return "\n".join(parts)


__all__ = [
    "EditKind",
    "LineEdit",
    "UnifiedHunk",
    "apply_replace_edits",
    "apply_line_replace_pairs",
    "apply_unified_diff",
    "replace_edits",
    "format_line_plan",
    "git_unified_diff",
    "join_lines",
    "line_edits",
    "line_edits_changes_only",
    "line_replace_pairs",
    "parse_unified_diff",
    "reconstruct_s2",
    "split_lines",
]
