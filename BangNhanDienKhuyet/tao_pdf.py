# -*- coding: utf-8 -*-
"""Tạo PDF "Bảng nhân điền khuyết" (bảng 2 đến bảng 9). Chạy: python3 tao_pdf.py"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))

W, H = A4
OUT = "Bang_Nhan_Dien_Khuyet_2_den_9.pdf"
COLORS = {2: "#E53935", 3: "#FB8C00", 4: "#F9A825", 5: "#43A047",
          6: "#00897B", 7: "#1E88E5", 8: "#5E35B1", 9: "#D81B60"}

# Kiểu ô trống cho 10 dòng: 'r' = trống kết quả, 'm' = trống thừa số thứ hai,
# 'g' = cho sẵn cả dòng. Mỗi bảng xoay một vị trí khác nhau.
BASE = ["r", "m", "r", "g", "r", "m", "r", "m", "r", "m"]

def pattern(n):
    k = (n - 2) % len(BASE)
    return BASE[k:] + BASE[:k]

def box(c, x, y, w, h, filled=None, col=None):
    c.setStrokeColor(colors.HexColor(col)); c.setLineWidth(1.4)
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
    if filled is not None:
        c.setFillColor(colors.HexColor("#2E7D32")); c.setFont("DVB", 16)
        c.drawCentredString(x + w / 2, y + 5, str(filled))

def table(c, n, x, y, w, h, answers=False):
    col = COLORS[n]
    c.setStrokeColor(colors.HexColor(col)); c.setLineWidth(2)
    c.setFillColor(colors.white); c.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    th = 1.3 * cm
    c.setFillColor(colors.HexColor(col)); c.roundRect(x, y + h - th, w, th, 10, stroke=0, fill=1)
    c.rect(x, y + h - th, w, th / 2, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont("DVB", 18)
    c.drawCentredString(x + w / 2, y + h - th + 0.4 * cm, f"BẢNG NHÂN {n}")
    pat = pattern(n)
    rh = (h - th - 0.4 * cm) / 10
    for i in range(1, 11):
        ry = y + h - th - 0.2 * cm - i * rh + (rh - 0.8 * cm) / 2 + 0.05 * cm
        bw, bh = 1.5 * cm, 0.8 * cm
        p = n * i
        t = pat[i - 1]
        # vị trí cột: n × i = p
        xs = x + 0.7 * cm
        xi, xp = xs + 2.9 * cm, xs + 5.1 * cm
        c.setFillColor(colors.black); c.setFont("DV", 17)
        c.drawString(xs, ry + 0.2 * cm, str(n))
        c.drawString(xs + 1.15 * cm, ry + 0.2 * cm, "×")
        c.drawString(xs + 4.4 * cm, ry + 0.2 * cm, "=")
        if t == "m":
            box(c, xs + 1.95 * cm - 0.25 * cm, ry, 1.2 * cm, bh, i if answers else None, col)
        else:
            c.setFillColor(colors.black); c.setFont("DV", 17)
            c.drawCentredString(xs + 2.2 * cm, ry + 0.2 * cm, str(i))
        if t == "r":
            box(c, xp - 0.15 * cm, ry, bw, bh, p if answers else None, col)
        else:
            c.setFillColor(colors.black); c.setFont("DV", 17)
            c.drawString(xp, ry + 0.2 * cm, str(p))

def header(c, title, sub):
    c.setFillColor(colors.HexColor("#263238")); c.setFont("DVB", 22)
    c.drawCentredString(W / 2, H - 1.8 * cm, title)
    c.setFont("DV", 11); c.setFillColor(colors.HexColor("#546E7A"))
    c.drawCentredString(W / 2, H - 2.5 * cm, sub)
    c.setFillColor(colors.black); c.setFont("DV", 11); c.setStrokeColor(colors.black)
    c.setLineWidth(0.5); c.setDash(1, 2)
    y = H - 3.4 * cm
    for lab, x0, x1 in (("Họ và tên:", 1.5, 11.5), ("Lớp:", 12, 15.5), ("Ngày:", 16, 19.5)):
        c.drawString(x0 * cm, y, lab)
        c.line((x0 + 0.1) * cm + c.stringWidth(lab, "DV", 11), y - 1, x1 * cm, y - 1)
    c.setDash()

def page(c, nums, title, sub, answers=False):
    header(c, title, sub)
    mx, gap = 1.5 * cm, 0.8 * cm
    tw = (W - 2 * mx - gap) / 2
    top = H - 4.2 * cm
    bottom = 1.5 * cm
    th = (top - bottom - gap) / 2
    for idx, n in enumerate(nums):
        r, k = divmod(idx, 2)
        table(c, n, mx + k * (tw + gap), top - (r + 1) * th - r * gap, tw, th, answers)
    c.showPage()

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Bảng nhân điền khuyết (bảng 2 đến bảng 9)"); c.setAuthor("")
SUB = "Điền số thích hợp vào ô trống"
page(c, [2, 3, 4, 5], "BẢNG NHÂN ĐIỀN KHUYẾT (1)", SUB)
page(c, [6, 7, 8, 9], "BẢNG NHÂN ĐIỀN KHUYẾT (2)", SUB)
page(c, [2, 3, 4, 5], "ĐÁP ÁN (1)", "Các số màu xanh là đáp án", True)
page(c, [6, 7, 8, 9], "ĐÁP ÁN (2)", "Các số màu xanh là đáp án", True)
c.save()
print("OK", OUT)
