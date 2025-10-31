import os
import json
import zipfile
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ----------------------------------------------------------
# НАСТРОЙКИ НА ШРИФТА
# ----------------------------------------------------------
try:
    # Ако добавиш Azbuki.ttf в static/, махни коментара на реда по-долу:
    # pdfmetrics.registerFont(TTFont('Azbuki', 'static/Azbuki.ttf'))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))  # fallback за кирилица
    FONT_NAME = "HeiseiMin-W3"
except:
    FONT_NAME = "Helvetica"

# ----------------------------------------------------------
# ДАННИ ЗА ОРГАНИЗАЦИЯТА
# ----------------------------------------------------------
ORG_FILE = "data.json"
if os.path.exists(ORG_FILE):
    with open(ORG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}

организация = data.get("организация", {
    "наименование": "Сдружение „Нова българска кухня“",
    "ЕИК": "208289975",
    "адрес": "гр. Варна, ж.к. Младост, бул. №108А, вх. 1, ет. 3, ап. 4",
    "телефон": "0899605928",
    "email": "newbgcuisine@gmail.com",
    "изготвил": "Ивайло (секретар)",
    "одобрил": "Калоян Йорданов Колев (председател)"
})

# ----------------------------------------------------------
# ВАЛУТНИ НАСТРОЙКИ
# ----------------------------------------------------------
EUR_RATE = 1.95583

def формат_валути(стойност_в_лева):
    """Връща стойността в лева и евро като низове."""
    левове = float(стойност_в_лева)
    евро = левове / EUR_RATE
    return f"{левове:,.2f}", f"{евро:,.2f}"

# ----------------------------------------------------------
# ГЛАВНА ФУНКЦИЯ ЗА СЪЗДАВАНЕ НА PDF
# ----------------------------------------------------------
def създай_pdf(име_на_файл, заглавие, таблици, година):
    папка = os.path.join("reports", str(година))
    os.makedirs(папка, exist_ok=True)
    път = os.path.join(папка, име_на_файл)

    doc = SimpleDocTemplate(път, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading", fontName=FONT_NAME, fontSize=14, alignment=1, spaceAfter=10))
    styles.add(ParagraphStyle(name="NormalBG", fontName=FONT_NAME, fontSize=11, leading=14))

    # Лого
    if os.path.exists("static/logo.png"):
        story.append(Image("static/logo.png", width=80, height=80))
        story.append(Spacer(1, 10))

    # Заглавна част
    header_text = f"""
    <b>{организация['наименование']}</b><br/>
    ЕИК: {организация['ЕИК']}<br/>
    {организация['адрес']}<br/>
    Тел.: {организация['телефон']} | Email: {организация['email']}<br/><br/>
    <b>{заглавие.upper()}</b><br/>
    Отчетен период: 01.01.{година} – 31.12.{година}<br/><br/>
    Курс: 1 EUR = 1.95583 BGN (фиксиран по Решение на БНБ)<br/><br/>
    """
    story.append(Paragraph(header_text, styles["NormalBG"]))
    story.append(Spacer(1, 12))

    # Таблици
    for t in таблици:
        таблица = Table(t, hAlign="LEFT")
        таблица.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))
        story.append(таблица)
        story.append(Spacer(1, 12))

    # Подписи
    дата = datetime.now().strftime("%d.%m.%Y %H:%M")
    подпис = f"""
    <br/><br/>
    Изготвил: _______________________ ({организация['изготвил']})<br/>
    Одобрил: _______________________ ({организация['одобрил']})<br/>
    Дата и час на изготвяне: {дата}
    """
    story.append(Paragraph(подпис, styles["NormalBG"]))

    doc.build(story)
    print(f"✅ Създаден файл: {път}")

# ----------------------------------------------------------
# ОТЧЕТИ
# ----------------------------------------------------------
def генерирай_баланс(данни):
    година = datetime.now().year
    таблица = [["АКТИВ", "Сума (лв.)", "Сума (евро)"]]
    активи = [
        ("Парични средства (501, 503)", 3200),
        ("Дълготрайни активи", 0),
        ("Други активи", 0),
    ]
    for име, лв in активи:
        лв_стр, евро_стр = формат_валути(лв)
        таблица.append([име, лв_стр, евро_стр])

    таблица += [["", "", ""], ["ПАСИВ", "Сума (лв.)", "Сума (евро)"]]
    пасиви = [
        ("Основен капитал (123)", 2000),
        ("Резерви и фондове", 500),
        ("Финансов резултат", 700),
    ]
    for име, лв in пасиви:
        лв_стр, евро_стр = формат_валути(лв)
        таблица.append([име, лв_стр, евро_стр])

    таблица.append(["", "", ""])
    таблица.append(["Курс: 1 EUR = 1.95583 BGN", "", ""])
    създай_pdf(f"Баланс_{година}.pdf", "Счетоводен баланс по НСС 9", [таблица], година)

def генерирай_опр(данни):
    година = datetime.now().year
    таблица = [["РАЗДЕЛ", "НАИМЕНОВАНИЕ", "Сума (лв.)", "Сума (евро)"]]
    редове = [
        ("I", "Приходи от нестопанска дейност (703)", 3000),
        ("II", "Приходи от дарения", 1200),
        ("III", "Разходи за материали (602)", 800),
        ("IV", "Разходи за възнаграждения", 1000),
        ("V", "Излишък (дефицит) за периода", 2400),
    ]
    for раздел, име, лв in редове:
        лв_стр, евро_стр = формат_валути(лв)
        таблица.append([раздел, име, лв_стр, евро_стр])

    таблица.append(["", "", "", ""])
    таблица.append(["Курс: 1 EUR = 1.95583 BGN", "", "", ""])
    създай_pdf(f"ОПР_{година}.pdf", "Отчет за приходите и разходите по НСС 9", [таблица], година)

def генерирай_справка_членове(данни):
    година = datetime.now().year
    членове = данни.get("членове", [
        {"име": "Петър Петров", "внос": 20},
        {"име": "Мария Иванова", "внос": 15},
        {"име": "Георги Георгиев", "внос": 30},
    ])
    таблица = [["Член", "Платен членски внос (лв.)", "Платен членски внос (евро)"]]
    for ч in членове:
        лв_стр, евро_стр = формат_валути(ч["внос"])
        таблица.append([ч["име"], лв_стр, евро_стр])
    таблица.append(["", "", ""])
    таблица.append(["Курс: 1 EUR = 1.95583 BGN", "", ""])
    създай_pdf(f"Справка_членски_внос_{година}.pdf", "Справка за членски внос", [таблица], година)

# ----------------------------------------------------------
# АРХИВИРАНЕ С MD5 ПОДПИС
# ----------------------------------------------------------
def архивирай_отчети(година):
    папка = os.path.join("reports", str(година))
    zip_path = os.path.join(папка, f"Отчети_{година}.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for файл in os.listdir(папка):
            if файл.endswith(".pdf"):
                zipf.write(os.path.join(папка, файл), файл)

    # MD5 подпис
    md5_hash = hashlib.md5()
    with open(zip_path, "rb") as f:
        md5_hash.update(f.read())
    md5_value = md5_hash.hexdigest()

    # Лог файл
    лог = os.path.join(папка, f"metadata_{година}.txt")
    with open(лог, "w", encoding="utf-8") as meta:
        meta.write(f"Отчети за {година}\n")
        meta.write(f"Създаден: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        meta.write(f"MD5 подпис: {md5_value}\n")
        meta.write(f"Файлове: {', '.join([f for f in os.listdir(папка) if f.endswith('.pdf')])}\n")
    print(f"📦 Архив създаден: {zip_path}")
    print(f"🔒 MD5 подпис: {md5_value}")

# ----------------------------------------------------------
# ГЛАВЕН ИНТЕРФЕЙС
# ----------------------------------------------------------
def генерирай_всички():
    if os.path.exists(ORG_FILE):
        with open(ORG_FILE, "r", encoding="utf-8") as f:
            данни = json.load(f)
    else:
        данни = {}
    генерирай_баланс(данни)
    генерирай_опр(данни)
    генерирай_справка_членове(данни)
    архивирай_отчети(datetime.now().year)

if __name__ == "__main__":
    генерирай_всички()
