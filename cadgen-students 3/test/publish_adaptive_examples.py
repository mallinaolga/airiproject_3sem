"""Copy existing exports and render a dimensional report, without meshing/generation."""

import argparse
import ast
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import shutil


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def number(value):return f"{value:.7g}" if value is not None else "н/д"
def triple(values):return " × ".join(number(v) for v in values)
def percentage(value):return number(value*100)+"%" if value is not None else "н/д"
def key(row):return f"{row['model']}-{row['joint_id']}"


def overlap_provenance(source):
    helper=Path(__file__).resolve().parents[1]/"cadgen/extrude.py"
    tree=ast.parse(helper.read_text())
    extrusion=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="extrude")
    defaults=dict(zip([a.arg for a in extrusion.args.args][-len(extrusion.args.defaults):],extrusion.args.defaults))
    default_world=ast.literal_eval(defaults["world_size"])
    translation=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="_surface_translation")
    assignment=next(n for n in ast.walk(translation) if isinstance(n,ast.Assign)
                    and any(isinstance(t,ast.Name) and t.id=="distance" for t in n.targets))
    assert isinstance(assignment.value,ast.BinOp) and isinstance(assignment.value.op,ast.Mult)
    coefficient=ast.literal_eval(assignment.value.left)
    programs=[]
    for folder in sorted(source.glob("model_*")):
        path=folder/"assembly/original.py";text=path.read_text();calls=[]
        for node in ast.walk(ast.parse(text)):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="extrude":
                supplied=len(node.args)>6 or any(k.arg=="world_size" for k in node.keywords)
                assert not supplied,"Explicit world_size requires separate provenance handling"
                calls.append(dict(line=node.lineno,source=ast.get_source_segment(text,node),
                                  world_size_argument_supplied=False,effective_default_world_size=default_world))
        programs.append(dict(model=folder.name,program_sha256=sha(path),extrude_calls=calls))
    return dict(helper="cadgen/extrude.py:_surface_translation",helper_sha256=sha(helper),
                coefficient=coefficient,default_world_size=default_world,
                translation_if_applicable_mm=coefficient*default_world,programs=programs,
                note="Static source inspection only. Applied when a prior shape and surface point exist. No per-joint CAD history replay performed.")


def write_report(audit,report,examples):
    rows=audit["joints"];small=[r for r in rows if r["below_001_mm"]]
    base=examples.relative_to(report.parent).as_posix()
    def part(row,name):return f"[{name}]({base}/{row['model']}/{name}.stl)"
    lines=["# Размеры установленных пазовых соединений AIRI", "",
        "Аудит **76 установленных соединений** в готовых `adaptive_joints_final`. "
        "Алгоритм, исходные детали и результаты сборки при аудите не менялись; генерация и поиск соединений не запускались.", "",
        f"[Все десять моделей: исходники, сборки и отдельные детали]({base}/README.md). "
        f"[Полные численные измерения JSON]({base}/joint_dimensions.json).", "",
        "## Что показали самые маленькие соединения", "",
        "**Нанометровый размер всех измерений не доказан как геометрически необходимый.** "
        "У 10 соединений ширина или глубина профиля меньше 0,01 мм. Девять из них расположены на "
        "контактных полосах шириной около **0,0005 мм**, уже присутствовавших в сохранённой декомпозиции. "
        "Эта узкая координата действительно ограничена. Но часто вдоль полосы доступны миллиметры "
        "или десятки миллиметров, а в глубину — 2–64 мм. "
        "Формула использует один радиус вписанной окружности для ограничения сразу трёх размеров "
        "и потому уменьшает также геометрически более свободные направления.", "",
        "**Откуда берётся 0,0005 мм:** в существующем [CADGen extrude.py](cadgen/extrude.py#L130) "
        "`_surface_translation()` задаёт служебный сдвиг `0.0000025 * world_size`. "
        "Все сохранённые программы выдавливания не передают этот аргумент, поэтому используется "
        "стандартное значение 200 и сдвиг равен **0,0005 мм**. Он применяется при присоединении "
        "к уже существующей поверхности. Измеренные полосы совпадают с этим служебным масштабом; "
        "их нельзя автоматически считать намеренно спроектированными элементами крепления. "
        "Это согласованный источник таких следов геометрии, но конкретная операция для каждого стыка "
        "в этом аудите заново не реконструировалась. "
        f"[Статическая проверка программ и контрольные суммы]({base}/cadgen_overlap_provenance.json).", "",
        "У 9 из этих 10 соединений `scale_factor=1`: повторного уменьшения масштаба не было. "
        "У модели №7, `e2`, выбран `0.08`, то есть дополнительное уменьшение в **12,5 раза**. "
        "Большие варианты отвергнуты проверкой Boolean-реконструкции, что не доказывает их геометрическую невозможность.", "",
        "Исключение по причине малой глубины — модель №2, `e2`: в выбранной точке "
        "приёмник имеет толщину всего **0,0005 мм**, хотя общий габарит детали намного больше. "
        "Ограничение глубины в этой точке подтверждается измерением. Оптимальность выбранного места не доказана.", "",
        "Это аудит имеющихся решений, а не новый поиск более крупных креплений. Изготовимость, "
        "прочность и механическое удержание не проверялись; дискретная проверка пути не доказывает непрерывную бесстолкновительность.", "",
        "## Метод и обозначения", "",
        "- Номера деталей совпадают с именами опубликованных `part_N.stl` после создания креплений. "
        "У моделей с 10 и более компонентами они могут отличаться от прежнего геометрического экспорта: "
        "соответствие сохранено в `component_id_map` и JSON аудита.",
        "- Габариты деталей **после креплений** — мировой XYZ, рассчитаны по B-Rep с отключённой "
        "триангуляцией (`AddOptimal`, `useTriangulation=False`). Габариты до креплений также сохранены в JSON.",
        "- Размеры стыка — ограничивающий прямоугольник **выбранной ограниченной грани** в системе XY соединения. "
        "S — площадь выбранной грани / сумма площадей всех плоских участков контакта этой пары, мм². "
        "Эти габариты сами по себе не считаются доказательством совместимости.",
        "- Профиль W × D × L: максимальная ширина профиля выступа (с учётом поднутрения), глубина и "
        "центральная длина зацепления из готовых метаданных. Ширина входа отдельно сохранена в JSON.",
        "- Паз Wп × Dп × Lп: **номинальные размеры полости с зазором** до обрезки инструментом по "
        "реальному телу приёмника: Wп=W+2c, Dп=D+c, Lп=L+2c. Это осевые размеры нормального офсета, "
        "а не максимальные размеры материала, реально удалённого из криволинейного тела. "
        "Для открытых скользящих пазов Lп относится к центральному зацеплению; полная длина приведена отдельно.",
        "- Отношения — **Wп / длина хорды X, Lп / длина хорды Y, Dп / глубина материала приёмника** "
        "в выбранной точке до креплений. Хорды взяты из точного пересечения прямой с ограниченной гранью; "
        "они не равны габаритам всей грани, если форма непpямоугольная.",
        "- Стенки измерены по готовому STEP в шести локальных направлениях. В таблице: "
        "дно / слева / справа / торец− / торец+ / основание выступа. Лучи из середины глубины паза "
        "находят первый интервал реального материала; основание измеряется по +Z из центра стыка. "
        "Это локальные линейные образцы, **не глобальная минимальная толщина**. Интервалы меньше "
        "20 допусков модели не сертифицируются; `н/д` также означает намеренно открытый торец. "
        "Точки, границы интервалов и погрешности сохранены в JSON. Параметр оболочки генератора "
        "не подменяет фактическую толщину стенки.", "",
        "## Все 76 соединений", "",
        "Сортировка по min(Wп,Dп,Lп), мм. **Жирным** отмечены случаи с шириной входа или глубиной профиля <0,01 мм. "
        "Все линейные величины — мм.", "",
        "| Модель / стык | Выступ → паз | Габариты донора XYZ | Габариты приёмника XYZ | Стык XY | S выбранная / вся пара | Профиль W×D×L | Паз Wп×Dп×Lп | c | Стенки: дно/лев./прав./−/+ /осн. | Wп/X; Lп/Y; Dп/H | Масштаб |",
        "|---|---|---|---|---|---:|---|---|---:|---|---|---:|"]
    for row in rows:
        walls=row["wall_samples_after"]
        ws=" / ".join(number(walls[k]["thickness_mm"]) for k in
                      ("receiver_floor","receiver_left","receiver_right","receiver_end_minus","receiver_end_plus","donor_anchor"))
        ratios=row["ratios"]
        rs="; ".join(percentage(ratios[k]) for k in ("nominal_cavity_width_over_contact_chord_x",
             "nominal_cavity_length_over_contact_chord_y","nominal_cavity_depth_over_receiver_material"))
        label=f"{int(row['model'][-2:])} / {row['joint_id']}"
        if row["below_001_mm"]:label=f"**{label}**"
        lines.append(f"| {label} | {part(row,row['donor'])} → {part(row,row['receiver'])} | "
            f"{triple(row['donor_dimensions_xyz_mm'])} | {triple(row['receiver_dimensions_xyz_mm'])} | "
            f"{triple(row['contact_face_dimensions_xy_mm'])} | {number(row['contact_face_area_mm2'])} / {number(row['pair_contact_area_mm2'])} | "
            f"{triple([row['profile_max_width_mm'],row['profile_depth_mm'],row['engagement_length_mm']])} | "
            f"{triple([row['nominal_cavity_width_mm'],row['nominal_cavity_depth_mm'],row['nominal_cavity_engagement_length_mm']])} | "
            f"{number(row['clearance_mm'])} | {ws} | {rs} | {number(row['selected_scale_factor'])} |")
    lines.extend(["", "## Соединения меньше 0,01 мм: причины выбора", ""])
    for row in small:
        d=row["profile_depth_mm"];radius=row["boundary_distance_at_center_mm"];factor=row["selected_scale_factor"]
        rd=row["receiver_depth_before_mm"];dd=row["donor_depth_before_mm"]
        sample=row["sampled_available_material"];range_r=[min(s["receiver_depth_mm"] for s in sample),max(s["receiver_depth_mm"] for s in sample)]
        ratios=row["ratios"]
        lines.extend([f"### Модель {int(row['model'][-2:])}, {row['joint_id']}: {row['donor']} → {row['receiver']}", "",
            f"Донор: **{triple(row['donor_dimensions_xyz_mm'])} мм**; приёмник: "
            f"**{triple(row['receiver_dimensions_xyz_mm'])} мм**. Выбранный стык: "
            f"**{triple(row['contact_face_dimensions_xy_mm'])} мм**, площадь {number(row['contact_face_area_mm2'])} мм². "
            f"Хорды через выбранный центр: {triple(row['face_chords_at_center_xy_mm'])} мм; "
            f"расстояние до ближайшей границы r={number(radius)} мм.", "",
            f"Профиль `{row['profile']['kind']}`: {triple([row['profile_max_width_mm'],d,row['engagement_length_mm']])} мм; "
            f"зазор {number(row['clearance_mm'])} мм. До креплений глубина материала по нормали: "
            f"приёмник **{number(rd)} мм**, донор **{number(dd)} мм**. "
            f"В {len(sample)} проверенных внутренних точках грани глубина приёмника "
            f"составляет {number(range_r[0])}–{number(range_r[1])} мм; это выборка, а не экстремум всей области.", ""])
        if row["size_cause"]=="receiver_depth":
            lines.append(f"Главная причина малой глубины — **реальный локальный слой {number(rd)} мм**: "
                f"ограничитель 0,35H={number(rd*.35)} мм меньше 0,6r={number(radius*.6)} мм. "
                "У круглого профиля ширина равна двум глубинам, поэтому ограничение глубины автоматически "
                "уменьшило ширину. Общий габарит приёмника не отражает толщину в этом месте. "
                "В выбранной ориентации глубина обоснована локальным материалом; необходимость столь малой ширины "
                "и длины, а также оптимальность места не доказаны.")
        else:
            lines.append(f"Глубину ограничил **r**, а не недостаток материала: 0,6r={number(radius*.6)} мм "
                f"при 0,35H={number(rd*.35)} мм. Та же величина задаёт начальные W≤1,05r и L≤1,25r; "
                "затем профиль равномерно вписывается в эти ограничения. "
                "Узкая координата контакта подтверждена, но перенос её ограничения на глубину и длинную "
                "координату является эвристикой поиска, а не доказанной необходимостью.")
        lines.extend(["",f"Выбранный масштаб **{number(factor)}**. "
            +( "Дополнительного уменьшения после начальной оценки стыка не было." if factor==1 else
               "Это дополнительное равномерное уменьшение относительно уже малого начального варианта."), "",
            f"Номинальный паз занимает {percentage(ratios['nominal_cavity_width_over_contact_chord_x'])} хорды X, "
            f"{percentage(ratios['nominal_cavity_length_over_contact_chord_y'])} хорды Y и "
            f"{percentage(ratios['nominal_cavity_depth_over_receiver_material'])} глубины материала приёмника.", ""])
        if row["matching_rejected_designs"]:
            lines.extend(["Сохранённые отказы той же конфигурации и того же места:", ""])
            for design in row["matching_rejected_designs"]:
                lines.append(f"- Масштаб `{number(design['scale_factor'])}`: `{design['reason']}`.")
            lines.extend(["", "Численные значения ошибки Boolean-реконструкции в этих старых отказах не сохранены. "
                "Этот журнал не позволяет отличить несовместимость формы от численной проблемы ядра. "
                "Повторное построение больших вариантов не выполнялось. Уменьшение до 0,08 нельзя считать "
                "доказанным требованием геометрии; это отдельный кандидат на дальнейшее исправление.", ""])
        lines.extend(["Локально измеренные остаточные стенки, мм:", "",
            "| Дно | Слева | Справа | Торец− | Торец+ | Основание выступа |","|---:|---:|---:|---:|---:|---:|"])
        lines.append("| "+" | ".join(number(row["wall_samples_after"][k]["thickness_mm"]) for k in
             ("receiver_floor","receiver_left","receiver_right","receiver_end_minus","receiver_end_plus","donor_anchor"))+" |")
        lines.append("")
    lines.extend(["## Длина открытых скользящих пазов", "",
        "Центральное зацепление нельзя выдавать за длину всего открытого паза. "
        "Ниже отдельно указаны длина инструмента с зазором и непрерывный участок приёмника "
        "на центральном срезе x=center, z=−D/2 до крепления. Последнее — точный локальный срез, "
        "а не глобальная длина всей криволинейной полости.", "",
        "| Модель / стык | Центральное зацепление | Полный инструмент | Участок приёмника на срезе |",
        "|---|---:|---:|---:|"])
    for row in rows:
        if row["sliding_receiver_middepth_span_mm"] is not None:
            lines.append(f"| {int(row['model'][-2:])} / {row['joint_id']} | {number(row['engagement_length_mm'])} | "
                f"{number(row['nominal_full_cutter_length_mm'])} | {number(row['sliding_receiver_middepth_span_mm'])} |")
    lines.extend(["", "## Как повторить без генерации", "", "```bash",
        "python test/audit_joint_dimensions.py --source examples/adaptive_joints --output /tmp/joint_dimensions.json", "```", "",
        "В публикацию включены исходные STEP, STEP деталей до креплений в `before/` и STEP деталей после креплений "
        "для воспроизводимости измерений. Все STL скопированы байт в байт из готового экспорта; "
        "отдельные `part_N.stl` всегда содержат детали **после** создания креплений. "
        "Отчёты поиска вынесены в связанные JSON без повторения одинаковых блоков. "
        "Старые примеры и алгоритм при подготовке публикации не изменялись.", ""])
    report.write_text("\n".join(lines),encoding="utf-8")


def publish(source,audit_file,output,report):
    source=Path(source).resolve();output=Path(output).resolve();report=Path(report).resolve()
    assert not output.exists(),"Preserving existing examples"
    assert not report.exists(),"Preserving existing report"
    audit=json.loads(Path(audit_file).read_text());assert audit["joints_count"]==76
    output.mkdir(parents=True)
    save(output/"joint_dimensions.json",audit)
    save(output/"cadgen_overlap_provenance.json",overlap_provenance(source))
    manifest=dict(source=str(source),generated_models=False,remeshed=False,models=[])
    summary=["# AIRI: адаптивные соединения десяти моделей", "",
        "Готовые результаты `adaptive_joints_final`: 86 основных деталей после креплений, "
        "76 установленных пазовых соединений. Новая генерация и изменение алгоритма не выполнялись.", "",
        "**Часть соединений микроскопическая.** Геометрическая проверка не подтверждает изготовимость "
        "или прочность. [Аудит всех 76 размеров и причин выбора](../../JOINT_DIMENSIONS.md). "
        "Пути проверены дискретно, непрерывная бесстолкновительность не доказана.", "",
        "Открывайте ссылки на STL для просмотра непосредственно на GitHub. Отдельные `part_N.stl` "
        "содержат обработанные детали; локальные координаты и размещение указаны в метаданных.", "",
        "| Модель | Частей | Пазов | Исходная модель | С креплениями, разобрана | С креплениями, собрана | Данные |",
        "|---|---:|---:|---|---|---|---|"]
    for model in sorted(source.glob("model_*")):
        src=model/"assembly"
        if not src.exists():continue
        target=output/model.name;target.mkdir()
        metadata=json.loads((src/"metadata.json").read_text());assert metadata["success"]
        model_rows=[r for r in audit["joints"] if r["model"]==model.name]
        assert len(model_rows)==len(metadata["joints"])
        copied={};aliases={}
        def transfer(old,new=None):
            new=new or old;destination=target/new;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(src/old,destination)
            assert sha(src/old)==sha(destination)
            copied[new]=dict(source=old,sha256=sha(destination),bytes=destination.stat().st_size)
            aliases[old]=new
        for name in ("original.stl","original.step","assembly.stl","assembly.step"):transfer(name)
        transfer("parts_exploded.stl","exploded.stl")
        for component in metadata["components"]:
            assert component["role"]=="main"
            transfer(component["stl"]);transfer(component["step"])
        for component in metadata["raw_components"]:
            old=component["step"];new=f"before/{component['name']}.step";transfer(old,new)
            component["step"]=new
            component.pop("stl",None)
        metadata["stl_exports"]={aliases[k]:v for k,v in metadata["stl_exports"].items()
                                 if k in aliases and aliases[k].endswith(".stl")}
        report_cache={}
        def compact(value):
            if isinstance(value,list):return [compact(v) for v in value]
            if not isinstance(value,dict):return value
            result={}
            for k,v in value.items():
                if k=="adaptive_search" and isinstance(v,dict):
                    digest=hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
                    relative=f"search_reports/{digest[:20]}.json"
                    if digest not in report_cache:save(target/relative,v);report_cache[digest]=relative
                    result[k]=dict(file=relative,sha256=sha(target/relative))
                elif k=="selected_edges" and isinstance(v,list):
                    result[k]=[dict(id=j["id"],components=j["components"]) for j in v]
                else:result[k]=compact(v)
            return result
        metadata=compact(metadata)
        for index,trial in enumerate(metadata["assembly_report"].get("trials",[]),1):
            alternatives=trial.pop("designs",None)
            if alternatives is not None:
                relative=f"alternatives/pair_{index:02d}.json";save(target/relative,alternatives)
                trial["options_file"]=relative
        metadata["publication"]=dict(source_folder=f"generations/assemblies/adaptive_joints_final/{model.name}/assembly",
            source_metadata_sha256=sha(src/"metadata.json"),source_schema_version=metadata["schema_version"],
            note="Existing CAD exports copied byte-for-byte; duplicate search reports referenced by file; no geometry generated.",
            copied_files=copied)
        metadata["schema_version"]=5;metadata["joint_dimensions_file"]="joint_dimensions.json"
        save(target/"metadata.json",metadata)
        save(target/"joint_dimensions.json",dict(units="mm",joints=model_rows))
        components=sorted(metadata["components"],key=lambda c:int(c["name"].split("_")[-1]))
        part_links=" · ".join(f"[{c['name']}]({c['stl']})" for c in components)
        name=model.name;count=len(components)
        readme=[f"# {name}: детали после создания креплений", "",
            "[Исходная цельная модель](original.stl) · [Разобранная с креплениями](exploded.stl) · "
            "[Сборка STL](assembly.stl) · [Сборка STEP](assembly.step)", "",
            "[Все соединения и размещения](metadata.json) · [Размеры соединений JSON](joint_dimensions.json) · "
            "[Общий аудит](../../../JOINT_DIMENSIONS.md)", "",
            "Все ссылки ниже ведут к STL деталей **после** создания пазов/выступов. "
            "Это локальные координаты деталей; трансформации в сборку сохранены в метаданных. "
            "Нумерация прежнего геометрического экспорта восстанавливается через `component_id_map`.", "",part_links,"",
            "| Деталь | STL после креплений | STEP после креплений | Габариты XYZ, мм | Номер в прежней декомпозиции |",
            "|---|---|---|---|---|"]
        inverse={v:k for k,v in metadata["component_id_map"].items()}
        for c in components:
            entry=next(r for r in model_rows if c["name"] in (r["donor"],r["receiver"]))
            dims=entry["donor_dimensions_xyz_mm"] if entry["donor"]==c["name"] else entry["receiver_dimensions_xyz_mm"]
            readme.append(f"| {c['name']} | [просмотр]({c['stl']}) | [STEP]({c['step']}) | {triple(dims)} | {inverse[c['name']]} |")
        readme.extend(["", "Для повторного B-Rep-аудита неизменённые STEP до креплений находятся в `before/`. "
            "Это вспомогательные входы измерений; исходные STL других примеров не заменялись. "
            "STL имеет ограниченную точность, особенно для микроскопических соединений; используйте STEP для точных измерений.", ""])
        (target/"README.md").write_text("\n".join(readme),encoding="utf-8")
        summary.append(f"| [{int(name[-2:])}]({name}/README.md) | {count} | {len(model_rows)} | "
            f"[STL]({name}/original.stl) | [STL]({name}/exploded.stl) | "
            f"[STL]({name}/assembly.stl) · [STEP]({name}/assembly.step) | "
            f"[Метаданные]({name}/metadata.json) · [Размеры]({name}/joint_dimensions.json) |")
        manifest["models"].append(dict(model=name,parts=count,joints=len(model_rows),files=copied,
                                       source_metadata_sha256=sha(src/"metadata.json")))
    summary.extend(["", "## Отдельные детали после креплений", ""])
    for model in manifest["models"]:
        name=model["model"]
        summary.append(f"- **Модель {int(name[-2:])}:** "+" · ".join(
            f"[part_{i}]({name}/part_{i}.stl)" for i in range(1,model["parts"]+1)))
    summary.extend(["", "STEP деталей до креплений опубликованы в `before/`, а STEP обработанных деталей — "
        "рядом с их STL, чтобы повторить аудит без генерации. "
        "`metadata.json` содержит все 76 установленных соединений по моделям, параметры профилей, зазоры, "
        "координатные преобразования и проверки. Повторяющиеся отчёты поиска вынесены в связанные JSON "
        "в `search_reports/`, альтернативы — в `alternatives/`.", "",
        "[Контрольные суммы скопированных готовых файлов](publication_manifest.json). "
        "Старые `examples/assemblies/` и `examples/two_stage_decomposition/` сохранены без изменений.", ""])
    assert len(manifest["models"])==10 and sum(m["joints"] for m in manifest["models"])==76
    (output/"README.md").write_text("\n".join(summary),encoding="utf-8")
    save(output/"publication_manifest.json",manifest)
    write_report(audit,report,output)
    return manifest


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",default="generations/assemblies/adaptive_joints_final")
    parser.add_argument("--audit",required=True)
    parser.add_argument("--output",default="examples/adaptive_joints")
    parser.add_argument("--report",default="JOINT_DIMENSIONS.md")
    args=parser.parse_args()
    result=publish(args.source,args.audit,args.output,args.report)
    print(f"Published {len(result['models'])} existing model exports; no generation or remeshing.")
