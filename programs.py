"""
Plan de estudios extraídos de los PDFs:
  - Major en Computación y Sistemas de Información Vs.02 (adm. 2025+)
  - Major en Ingeniería Eléctrica Vs.03 (adm. 2025+)
  - Minor de Amplitud (versiones vigentes)

Formato:
  PROGRAMS[key] = {"name": str, "kind": "major"|"minor",
                   "sections": [(titulo, "req"|"opt", [items], creditos)]}
  Un item es una sigla ("MAT1203") o una lista de alternativas
  (["FIS1514", "ICE1514"]  ==  "FIS1514 o ICE1514").
  "req" = cursos mínimos/obligatorios, "opt" = listas de optativos.
  creditos = créditos que exige esa área según el PDF (None = complementarios/reemplazo).
"""

# ---------------------------------------------------------------- nombres
NAMES = {
    # Plan común
    "MAT1610": "Cálculo I", "QIM100E": "Química para Ingeniería", "MAT1620": "Cálculo II",
    "FIS1514": "Dinámica", "ICE1514": "Dinámica", "FIS0154": "Laboratorio de Dinámica",
    "ICS1513": "Introducción a la Economía", "IIC1103": "Introducción a la Programación",
    "FIS1523": "Termodinámica", "IIQ1003": "Termodinámica", "ICM1003": "Termodinámica",
    "IIQ103H": "Termodinámica Honors", "FIS0152": "Laboratorio de Termodinámica",
    "EYP1113": "Probabilidades y Estadística", "FIS1533": "Electricidad y Magnetismo",
    "IEE1533": "Fundamentos de Teoría Electromagnética",
    "FIS0153": "Laboratorio de Electricidad y Magnetismo",
    "ING2030": "Investigación, Innovación y Emprendimiento",
    "BIO110C": "Biología de Organismos y Comunidades", "BIO141C": "Biología de la Célula",
    "BIO135C": "Fisiología", "BIO143M": "Principios Ecológicos y Medio Ambiente",
    "FIL2001": "Filosofía, ¿para qué?",
    "MAT1203": "Álgebra Lineal", "ING1004": "Desafíos de la Ingeniería",
    "MAT1630": "Cálculo III", "MAT1640": "Ecuaciones Diferenciales",
    # Exploración de major
    "AQH0000": "Introducción a la Arquitectura", "IBM1005": "Introducción a la Ingeniería Biomédica",
    "ICC1001": "Introducción a la Ingeniería Civil", "ICC2304": "Ingeniería de Construcción",
    "ICE2006": "Estática", "ICE2623": "Introducción a la Geología Física", "IMM2003": "Geología Minera",
    "ICH1005": "Desafíos en Recursos Hídricos y Medio Ambiente", "ICH1104": "Mecánica de Fluidos",
    "ICH2304": "Ingeniería Ambiental", "ICM1002": "Diseño Gráfico en Ingeniería Mecánica",
    "ICS1113": "Optimización", "ICS113H": "Optimización-Honors",
    "ICT1103": "Transporte y Logística: Cómo se mueve el mundo", "IDI1015": "Pensamiento Visual",
    "IEE1100": "Introducción a la Ingeniería Eléctrica", "IEE2103": "Señales y Sistemas",
    "IEE2123": "Circuitos Eléctricos", "IFI1001": "Introducción a la Ingeniería Física",
    "IIC1005": "Computación: Ciencia y Tecnología del Mundo Digital",
    "IIQ1001": "Introducción a la Ingeniería Química", "IIQ2663": "Fundamentos de Biotecnología",
    "IIQ2930": "Introducción a la Ingeniería Gastronómica", "IMM1003": "Introducción a la Minería",
    "IMT1001": "Introducción a la Ingeniería Matemática",
    "IRB1010": "Introducción Exploratoria a la Robótica", "IRB2001": "Fundamentos de Robótica",
    # Computación
    "IIC1253": "Matemáticas Discretas", "IIC2133": "Estructuras de Datos y Algoritmos",
    "IIC2143": "Ingeniería de Software", "IIC2233": "Programación Avanzada",
    "IIC2413": "Bases de Datos", "IIC2513": "Tecnologías y Aplicaciones Web",
    "IIC2531": "Seguridad Computacional", "IIC2154": "Proyecto de Especialidad (Capstone)",
    "IIC2343": "Arquitectura de Computadores", "IIC2333": "Sistemas Operativos y Redes",
    "IIC2613": "Inteligencia Artificial", "IIC2713": "Sistemas de Información",
    "IIC2733": "Modelos de Procesos", "IIC2764": "Conocimiento, Cultura y Tecnología",
    "IIC2213": "Lógica para Ciencias de la Computación",
    "IIC2223": "Teoría de Autómatas y Lenguajes Formales",
    "IIC2283": "Diseño y Análisis de Algoritmos", "IIC2523": "Sistemas Distribuidos",
    "IIC3253": "Criptografía y Seguridad Computacional", "IIC2433": "Minería de Datos",
    "EYP2114": "Inferencia Estadística", "IIC2026": "Visualización de Información",
    "IIC3757": "Minería de Procesos", "IIC3695": "Tópicos Avanzados en Inteligencia de Máquina",
    "IIC3633": "Sistemas Recomendadores", "IIC3413": "Implementación de Sistemas de Base de Datos",
    "IIC3432": "Tópicos Avanzados en Bases de Datos", "IIC3423": "Big Data",
    "IIC3640": "Modelos Gráficos Probabilísticos",
    "IIC3692": "Tópicos Avanzados en Inteligencia Artificial", "IIC3724": "Reconocimiento de Patrones",
    "EYP230I": "Análisis de Regresión", "EYP280I": "Métodos Bayesianos",
    "ICS2123": "Modelos Estocásticos", "IIC2440": "Procesamiento de Datos Masivos",
    "IIC2115": "Programación Como Herramienta para Ingeniería",
    "IIC2985": "Investigación o Proyecto", "IIC2986": "Investigación o Proyecto",
    "IIC2987": "Investigación o Proyecto",
    # Eléctrica
    "IEE2513": "Comunicaciones", "IEE2183": "Laboratorio de Mediciones Eléctricas",
    "IEE2473": "Laboratorio de Electrónica Analógica y Digital", "IEE2113": "Teoría Electromagnética",
    "IEE2913": "Diseño Eléctrico (Capstone)", "IEE2413": "Electrónica", "IEE2713": "Sistemas Digitales",
    "IEE2213": "Máquinas Eléctricas", "IEE2613": "Control Automático",
    "IEE1133": "Materiales Eléctricos", "ING1024": "Propiedades y Resistencia de Materiales",
    "QIM200": "Química Orgánica Fundamental", "ING2045": "Introducción a la Sustentabilidad",
    "ING2055": "Análisis y Aplicación de Observaciones Geoespaciales",
    "ING2050": "Desarrollo y Aplicaciones de Sistemas Aéreos No Tripulados",
    "ETI188": "Ética para Ingeniería", "IEE2463": "Sistemas Electrónicos Programables",
    "IEE2273": "Laboratorio de Máquinas Eléctricas", "IEE2683": "Laboratorio de Control Automático",
    "IEE2573": "Laboratorio de Telecomunicaciones", "IEE2690": "Laboratorio de Sistemas Ciberfísicos",
    "IBM2012": "Monitoreo Fisiológico y Análisis de Datos", "IBM2101": "Imágenes Biomédicas",
    "ICS2121": "Métodos de Optimización",
    # Minors de amplitud
    "ICH2204": "Hidrología", "ICH2114": "Ingeniería Hidráulica", "ICH2314": "Calidad del Agua",
    "ICM2223": "Transferencia de Calor", "IIQ2363": "Residuos Sólidos y Peligrosos",
    "ICH2604": "Principios de Tratamiento de Aguas",
    "ICH2613": "CMD Cambio Climático: un Enfoque Multidisciplinario",
    "GEO202": "Sistemas de Información Geográfica", "ICE2313": "Mecánica de Sólidos",
    "ICE2604": "Fundamentos de Geotecnia", "ICC2105": "Materiales de Ingeniería Civil",
    "ICE2614": "Mecánica de Suelos", "ICE2630": "Geofísica General", "ICE3653": "Mecánica de Rocas",
    "ICE2633": "Geología Estructural y Tectónica", "ICE2640": "Recursos y Exploración Geológica",
    "ICH2214": "Agua Subterránea", "IMM2033": "Geoestadística",
    "IMM2213": "Fundamentos de la Economía de Minerales", "IMM2013": "Minería a Cielo Abierto",
    "IMM2043": "Minería Subterránea", "ICE2643": "Métodos Geofísicos para Ingeniería",
    "ICE2028": "Mineralogía y Petrología",
    "ICE2029": "Procesos Superficiales y Peligros Geológicos",
    "GEO612": "El Desierto de Atacama, Pasado, Presente y Futuro",
    "GEO3086": "Principios de Volcanología", "ICE2135": "Métodos Numéricos en Ingeniería",
    "ICE2114": "Análisis Estructural I", "ICE2413": "Hormigón Armado",
    "ICE2533": "Estructuras de Acero", "ICC2454": "Diseño y Construcción en Madera",
    "ICE2703": "Ingeniería Antisísmica", "ICM2403": "Ciencia de los Materiales",
    "ICM2028": "Mecánica de Materiales", "ICM2022": "Diseño Mecánico",
    "ICM2213": "Conversión de Energía", "ICM2503": "Procesos de Manufactura",
    "ICM2803": "Dinámica de Sistemas Mecánicos", "ICM2985": "Investigación o Proyecto",
    "IMM2023": "Procesos Mineralúrgicos", "IMM2053": "Procesos Metalúrgicos",
    "IMM2073": "Minería Sustentable", "IMM2985": "Investigación o Proyecto",
    "IMM2986": "Investigación o Proyecto", "IMM2987": "Investigación o Proyecto",
    "ICT2233": "Flujo en Redes", "ICT2904": "Ingeniería de Sistemas de Transporte",
    "ICT2213": "Modelos de Demanda de Transporte", "ICT2223": "Modelos de Tráfico",
    "ICT2303": "Tecnología de Medios de Transporte", "ICT2443": "Ingeniería Logística",
    "ICT3443": "Ingeniería Logística", "ICT2985": "Investigación o Proyecto",
    "ICT2986": "Investigación o Proyecto", "ICT2987": "Investigación o Proyecto",
    "ICS2523": "Microeconomía", "ICS2613": "Contabilidad y Control de Gestión",
    "ICS2813": "Organización y Comportamiento en la Empresa",
    "ICS2133": "Fundamentos de Simulación de Sistemas Estocásticos",
    "ICS2562": "Econometría Aplicada", "QIM106A": "Química Inorgánica I",
    "QIM106B": "Química Inorgánica I", "IIQ2003": "Fenómenos de Transporte",
    "IIQ2043": "Fisicoquímica", "IIQ2133": "Procesos Químicos",
    "IIQ2013": "Operaciones Unitarias I", "IIQ2023": "Operaciones Unitarias II",
    "BIO151E": "Biología de Microorganismos", "IIQ2693": "Biotecnología Molecular",
    "BIO228C": "Bioquímica y Genética Molecular", "BIO252I": "Ingeniería Genética y Bioinformática",
    "IIQ2113": "Diseño de Reactores", "IIQ2673": "Bioseparaciones",
    "MAT2605": "Cálculo Científico I", "MAT251I": "Análisis Real",
    "IMT2111": "Álgebra Lineal Numérica",
    "IMT2112": "Algoritmos Paralelos en Computación Científica",
    "IMT2113": "Análisis de Fourier Aplicado", "IMT2115": "Control de Sistemas Lineales",
    "MAT250I": "Ecuaciones Diferenciales Parciales", "MAT2205": "Álgebra Abstracta I",
    "MAT2305": "Geometría Diferencial", "MAT2415": "Lógica", "MAT2545": "Topología",
    "MAT255I": "Análisis Funcional", "MAT270I": "Variable Compleja I",
    "MAT253I": "Teoría de Integración", "MAT2615": "Cálculo Científico II",
    "MAT2320": "Introducción a Métodos Matemáticos para Aprendizaje Profundo",
    "ICC2204": "Planificación y Control de Proyectos", "ICC2424": "Construcción de Obras Civiles",
    "ICC2514": "Ingeniería Vial", "ICC2414": "Topografía y Geoinformación Aplicada",
    "ICC2354": "Diseño de Edificios Sustentables", "ICC3464": "Sustentabilidad en la Construcción",
    "ICC3470": "Construcción Avanzada de Túneles", "ICC2312": "Instalaciones en Edificios",
    "ICC2913": "Tecnologías de Información en Construcción",
    "ICS3223": "Gestión Logística", "ICS3723": "Simulación",
    "ICT3463": "Métodos Avanzados para Sistemas de Transporte y Logística",
    "ICT3352": "Teoría de Colas", "ICT3454": "Análisis de Sistemas Logísticos",
    "ICT3464": "Ruteo de Vehículos",
    "IDI2031": "Prototipado y Validación de Innovaciones Tecnológicas",
    "ICS2031": "Estrategia y Comercialización de Innovaciones Tecnológicas",
    "ICS2032": "Financiamiento y Creación de Start-Ups",
    "ING2031": "Vigilancia Tecnológica e Inteligencia Competitiva",
    "DEM298": "Propiedad Intelectual y Transferencia Tecnológica",
    "IIQ2343": "Contaminación Atmosférica", "ICT2253": "Externalidades de Transporte",
    "ICT3103": "Economía de Transporte", "ICT3244": "Modelos Econométricos en Ingeniería",
}

# ---------------------------------------------------------------- créditos por curso (PDF)
# Por defecto 10 cr. buscacursos.uc.cl, si responde, tiene prioridad.
CREDITS = {s: 10 for s in NAMES}
CREDITS.update({
    "FIS0154": 0, "FIS0152": 0, "FIS0153": 0,
    "IEE2183": 5, "IEE2473": 5, "IEE2273": 5, "IEE2683": 5, "IEE2573": 5,
    "ING2031": 5, "DEM298": 5, "ICT3352": 5, "ICT3454": 5,
})

# ---------------------------------------------------------------- secciones compartidas
PLAN_COMUN = [
    ("1.1 Ciencias básicas (mínimos)", "req", [
        "MAT1610", "QIM100E", "MAT1620", ["FIS1514", "ICE1514"], "FIS0154", "ICS1513",
        "IIC1103", ["FIS1523", "IIQ1003", "ICM1003", "IIQ103H"], "FIS0152", "EYP1113",
        ["FIS1533", "IEE1533"], "FIS0153", "ING2030",
    ], 120),
    ("1.1 Optativo Biológico", "opt", ["BIO110C", "BIO141C", "BIO135C", "BIO143M"], 10),
    ("1.2 Formación General (FIL2001 + Teológico + 60 cr electivos)", "req", ["FIL2001"], 80),
    ("1.3 Base general para Major (mínimos)", "req", ["MAT1203", "ING1004", "MAT1630", "MAT1640"], 40),
    ("1.3 Optativo de Exploración de Major", "opt", [
        "AQH0000", "IBM1005", "ICC1001", "ICC2304", "ICE2006", ["ICE2623", "IMM2003"],
        "ICH1005", "ICH1104", "ICH2304", "ICM1002", ["ICS1113", "ICS113H"], "ICT1103",
        "IDI1015", "IEE1100", "IEE2103", "IEE2123", "IFI1001", "IIC1005", "IIQ1001",
        "IIQ2663", "IIQ2930", "IMM1003", "IMT1001", ["IRB1010", "IRB2001"],
    ], 10),
]

COMP_MAJOR = [
    ("1.1 Optativo de Fundamentos (obligatorio en este Major)", "req", ["IIC1253"], 10),
    ("2. Major — Mínimos", "req",
     ["IIC2133", "IIC2143", "IIC2233", "IIC2413", "IIC2513", "IIC2531", "IIC2154"], 70),
]

ELEC_MAJOR = [
    ("1.1 Optativo de Fundamentos de Ciencias o Ingeniería", "opt", [
        "ICE2006", ["ICE2623", "IMM2003"], "ICH1104", ["ICS1113", "ICS113H"], "IEE1133",
        "IEE2103", "IEE2123", "IIC1253", "IIQ2663", "ING1024", "QIM200", "ING2045",
        "ING2055", "IIQ2930", "ING2050", "IIC2233", "ETI188",
    ], 10),
    ("2. Major — Mínimos", "req", [
        "IEE2103", "IEE2123", "IEE2513", "IEE2183", "IEE2473", "IEE2113", "IEE2913",
        "IEE2413", "IEE2713", "IEE2213", "IEE2613",
    ], 100),
]

COMPL = "Optativos Complementarios (si ya aprobaste un mínimo)"

# ---------------------------------------------------------------- programas
PROGRAMS = {
    "M296": {"name": "(M296) Computación y Sist. de Información — Track Computación Vs.02",
             "kind": "major",
             "sections": PLAN_COMUN + COMP_MAJOR + [
                 ("2. Track Computación — Mínimos", "req", ["IIC2343", "IIC2333", "IIC2613"], 30)]},
    "M297": {"name": "(M297) Computación y Sist. de Información — Track Sistemas de Información Vs.02",
             "kind": "major",
             "sections": PLAN_COMUN + COMP_MAJOR + [
                 ("2. Track Sistemas de Información — Mínimos", "req",
                  ["IIC2713", "IIC2733", "IIC2764"], 30)]},
    "M233": {"name": "(M233) Ingeniería Eléctrica Vs.03", "kind": "major",
             "sections": PLAN_COMUN + ELEC_MAJOR},
    "PLAN": {"name": "Solo Plan Común de Licenciatura", "kind": "major", "sections": PLAN_COMUN},

    # ------------------------------------------------------------ minors de profundidad
    "N160": {"name": "(N160) Profundidad: Fundamentos Científicos y Tecnológicos de la Computación Vs.02",
             "kind": "minor", "for": ["M296", "M297"],
             "sections": [
                 ("Minor — Mínimos (requiere IIC2333 aprobado)", "req",
                  ["IIC2213", "IIC2223", "IIC2283", "IIC2523"], 40),
                 ("Minor — Optativos", "opt", ["IIC2333", "IIC2343", "IIC2613", "IIC3253"], 10)]},
    "N161": {"name": "(N161) Profundidad: Data Science y Analytics Vs.01",
             "kind": "minor", "for": ["M296", "M297"],
             "sections": [
                 ("Minor — Mínimos", "req", ["IIC2433", "EYP2114", "IIC2026", "IIC2613"], 40),
                 ("Minor — Optativos", "opt", [
                     "IIC3757", "IIC3695", "IIC3633", "IIC3413", "IIC3432", "IIC3423", "IIC3640",
                     "IIC3692", "IIC3724", "EYP230I", "EYP280I", "ICS2123", "IIC2440"], 10)]},
    "N343": {"name": "(N343) Profundidad: Ingeniería Eléctrica", "kind": "minor", "for": ["M233"],
             "sections": [
                 ("Minor — Mínimos", "req", ["IEE2463"], 10),
                 ("Minor — Optativos de laboratorio", "opt",
                  ["IEE2273", "IEE2683", "IEE2573", "IEE2690"], 10),
                 ("Minor — Optativos", "opt", [
                     "IBM2012", "IBM2101", "IIC2233", "IIC2115", "IRB2001", "ICS2121"], 30)]},

    # ------------------------------------------------------------ minors de amplitud
    "N338": {"name": "(N338) Amplitud: Ingeniería Hidráulica y Ambiental Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICH1104", "ICH2204", "ICH2114", "ICH2304", "ICH2314"], 50),
                 (COMPL, "opt", ["ICM2223", "IIQ2363", "ICH2604", "ICH2613", "ICE2623", "GEO202"], None)]},
    "N776": {"name": "(N776) Amplitud: Programación Vs.01", "kind": "minor", "excluded": ["M296", "M297"],
             "sections": [
                 ("Minor — Mínimos", "req", ["IIC1253", "IIC2133", "IIC2143", "IIC2233", "IIC2413"], 50),
                 (COMPL, "opt", ["IIC2343", "IIC2713", "IIC2513", "IIC2613", "IIC2333", "IIC2283"], None)]},
    "N207": {"name": "(N207) Amplitud: Tecnologías de la Información Vs.01", "kind": "minor",
             "excluded": ["M296", "M297"],
             "sections": [
                 ("Minor — Mínimos", "req", ["IIC2233", "IIC2413", "IIC2733", "IIC2764", "IIC2713"], 50),
                 (COMPL, "opt", ["IIC2513", "IIC2433", "IIC2613", "IIC2985", "IIC2986", "IIC2987"], None)]},
    "N346": {"name": "(N346) Amplitud: Ingeniería Estructural Vs.02", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICE2114", "ICE2313", "ICE2006", "ICC2105"], 40),
                 ("Minor — Mínimos (elegir uno)", "opt", ["ICE2413", "ICE2533", "ICC2454"], 10),
                 (COMPL, "opt", ["ICE2413", "ICE2533", "ICC2454", "ICE2703"], None)]},
    "N345": {"name": "(N345) Amplitud: Ingeniería Geotécnica Vs.02", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICE2313", "ICE2604", "ICE2623", "ICE2006", "ICC2105"], 50),
                 (COMPL, "opt", ["ICE2614", "ICE2630", "ICE3653"], None)]},
    "N202": {"name": "(N202) Amplitud: Geociencias — Área Recursos Geológicos Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICE2623", "ICE2630", "ICE2633"], 30),
                 ("Área Recursos Geológicos — Mínimo", "req", ["ICE2640"], 10),
                 ("Área Recursos Geológicos — Elegir", "opt", [
                     "ICH1104", "ICH2204", "ICH2214", "ICH2114", "IMM2033", "IMM2213", "IMM2013",
                     "IMM2043", "ICE2643", "ICE2028"], 10)]},
    "N203": {"name": "(N203) Amplitud: Geociencias — Área Peligros Geológicos Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICE2623", "ICE2630", "ICE2633"], 30),
                 ("Área Peligros Geológicos — Mínimo", "req", ["ICE2029"], 10),
                 ("Área Peligros Geológicos — Elegir", "opt",
                  ["GEO202", "GEO612", "GEO3086", "ICE2135", "ICE2643"], 10)]},
    "N678": {"name": "(N678) Amplitud: Ingeniería Mecánica Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", [["ING1024", "ICM2403"], ["ICM2028", "ICE2313"], "ICM2022",
                                             "ICH1104", "ICM2223"], 50),
                 (COMPL, "opt", ["ICM2213", "ICM2503", "ICM2803", "ICM2985"], None)]},
    "N289": {"name": "(N289) Amplitud: Ingeniería Minera Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["IMM2013", "IMM2023", "IMM2043", ["IMM2003", "ICE2623"]], 40),
                 ("Minor — Optativos", "opt", [
                     "IMM2033", "IMM2053", "IMM2073", "IMM2985", "IMM2986", "IMM2987"], 10)]},
    "N682": {"name": "(N682) Amplitud: Sistemas de Transporte Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICS1113", "ICT2233", "ICT2904"], 30),
                 ("Minor — Optativos", "opt", [
                     "ICT2213", "ICT2223", "ICT2303", ["ICT2443", "ICT3443"], "ICT2985", "ICT2986",
                     "ICT2987", "IIC2115", "IIC2233"], 20)]},
    "N200": {"name": "(N200) Amplitud: Ingeniería Industrial Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", [["ICS1113", "ICS113H"], "ICS2123", "ICS2523", "ICS2613",
                                             "ICS2813"], 50),
                 (COMPL, "opt", ["ICS2121", "ICS2133", "ICS2562", ["IIC2233", "IIC2115"]], None)]},
    "N201": {"name": "(N201) Amplitud: Logística y Transporte de Carga Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICS1113", "ICS2123", "ICT2233", "ICT2904"], 40),
                 ("Minor — Optativos", "opt", [
                     "ICS3223", ["ICS2133", "ICS3723"], ["ICT2443", "ICT3443"], "ICT2303", "ICT3463",
                     "ICT3352", "ICT3454", "ICT3464", "ICT2985", "ICT2986", "ICT2987", "IIC2115"], 10)]},
    "N229": {"name": "(N229) Amplitud: Ingeniería Química Vs.02", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", [["QIM106A", "QIM106B"], "IIQ2003", "IIQ2043", "IIQ2133",
                                             "QIM200"], 50),
                 (COMPL, "opt", ["IIQ2013", "IIQ2023"], None)]},
    "N235": {"name": "(N235) Amplitud: Fundamentos de Ingeniería Biológica Vs.02", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["BIO141C", "BIO151E", "IIQ2663", "IIQ2693", "QIM200"], 50),
                 (COMPL, "opt", ["BIO228C", "BIO252I", "IIQ2133", "IIQ2043", "IIQ2113", "IIQ2673"], None)]},
    "N205": {"name": "(N205) Amplitud: Matemáticas Aplicadas Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["MAT2605", "MAT251I"], 20),
                 ("Minor — Optativos", "opt", [
                     "EYP2114", "EYP280I", ["ICS1113", "ICS113H"], "IIC1253", "IMT2111", "IMT2112",
                     "IMT2113", "IMT2115", "MAT250I", "MAT2205", "MAT2305", "MAT2415", "MAT2545",
                     "MAT255I", "MAT270I", "MAT253I", "MAT2615", "MAT2320"], 30)]},
    "N206": {"name": "(N206) Amplitud: Ingeniería Matemática Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["MAT2605", "MAT251I", "IIC1253", "MAT253I", "EYP2114"], 50),
                 (COMPL, "opt", [
                     "ICS113H", "IIC2233", "IMT2111", "IMT2112", "IMT2113", "IMT2115", "MAT255I",
                     "MAT2615", "MAT2320"], None)]},
    "N344": {"name": "(N344) Amplitud: Ingeniería Eléctrica Vs.02", "kind": "minor", "excluded": ["M233"],
             "sections": [
                 ("Minor — Mínimos", "req", ["IEE2103", "IEE2123", "IEE2713", "IEE2613"], 40),
                 ("Minor — Cualquier curso IEE nivel 2000", "opt", [], 10)]},
    "N231": {"name": "(N231) Amplitud: Ingeniería de Construcción Vs.02", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["ICC2105", "ICC2204", "ICC2304"], 30),
                 ("Minor — Optativos", "opt", ["ICE2006", "ICE2313", "ICE2604", "ICC2424", "ICC2514"], 20),
                 (COMPL, "opt", [
                     "ICC2454", "ICC2414", "ICC2354", "ICC3464", "ICC3470", "ICC2312", "ICC2913"], None)]},
    "N242": {"name": "(N242) Amplitud: Innovación Tecnológica Vs.01", "kind": "minor",
             "sections": [
                 ("Minor — Mínimos", "req", ["IDI2031", "ICS2031", "ICS2032", "ING2031", "DEM298"], 40),
                 ("Minor — Optativos (Escuela de Ingeniería)", "opt", [], 10)]},
}


def program_courses(key):
    """Todas las siglas (aplanando alternativas) de un programa."""
    out = []
    for _title, _kind, items, *_ in PROGRAMS[key]["sections"]:
        for it in items:
            for s in (it if isinstance(it, list) else [it]):
                if s not in out:
                    out.append(s)
    return out
