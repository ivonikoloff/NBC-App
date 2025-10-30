import os
import json
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
    # ако добавиш Azbuki.ttf в static/, махни коментара на долния ред:
    # pdfmetrics.registerFont(TTFont('Azbuki', 'static/Azbuki.ttf'))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))  # fallback за кирилица
    FONT_NAME = "HeiseiMin-W3"
except:
    FONT_NAME = "Helvetica"

# ----------------------------------------------------------
# ДАННИ ЗА ОРГАНИЗАЦИЯТА
# ----------------------------------------------------------
ORG_FILE = "data.json"
with open(ORG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

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
    """
    story.append(Paragraph(header_text, styles["NormalBG"]))
    story.append(Spacer(1, 12))

    # Таблици (списъци с редове)
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
    дата = datetime.now().strftime("%d.%m.%Y")
    подпис = f"""
    <br/><br/>
    Изготвил: _______________________ ({организация['изготвил']})<br/>
    Одобрил: _______________________ ({организация['одобрил']})<br/>
    Дата: {дата}
    """
    story.append(Paragraph(подпис, styles["NormalBG"]))

    doc.build(story)
    print(f"✅ Създаден файл: {път}")

# ----------------------------------------------------------
# ОТЧЕТИ
# ----------------------------------------------------------
def генерирай_баланс(данни):
    година = datetime.now().year
    таблица = [
        ["АКТИВ", "Сума (лв.)"],
        ["Парични средства (501, 503)", "3 200"],
        ["Дълготрайни активи", "0"],
        ["Други активи", "0"],
        ["", ""],
        ["ПАСИВ", "Сума (лв.)"],
        ["Основен капитал (123)", "2 000"],
        ["Резерви и фондове", "500"],
        ["Финансов резултат", "700"]
    ]
    създай_pdf("Баланс_" + str(година) + ".pdf", "Счетоводен баланс по НСС 9", [таблица], година)

def генерирай_опр(данни):
    година = datetime.now().year
    таблица = [
        ["РАЗДЕЛ", "НАИМЕНОВАНИЕ", "СУМА (лв.)"],
        ["I", "Приходи от нестопанска дейност (703)", "3 000"],
        ["II", "Приходи от дарения", "1 200"],
        ["III", "Разходи за материали (602)", "800"],
        ["IV", "Разходи за възнаграждения", "1 000"],
        ["V", "Излишък (дефицит) за периода", "2 400"]
    ]
    създай_pdf("ОПР_" + str(година) + ".pdf", "Отчет за приходите и разходите по НСС 9", [таблица], година)

def генерирай_справка_членове(данни):
    година = datetime.now().year
    членове = данни.get("членове", [])
    таблица = [["Член", "Платен членски внос (лв.)"]]
    for ч in членове:
        таблица.append([ч["име"], f"{ч['внос']:.2f}"])
    създай_pdf("Справка_членски_внос_" + str(година) + ".pdf", "Справка за членски внос", [таблица], година)

# ----------------------------------------------------------
# ГЛАВЕН ИНТЕРФЕЙС
# ----------------------------------------------------------
def генерирай_всички():
    with open(ORG_FILE, "r", encoding="utf-8") as f:
        данни = json.load(f)
    генерирай_баланс(данни)
    генерирай_опр(данни)
    генерирай_справка_членове(данни)

if __name__ == "__main__":
    генерирай_всички()
