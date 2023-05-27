import pygame as pg
import qrcode
import sys
import button
import textbox


def main() -> None:

    pg.init()

    window = pg.display.set_mode((1000, 750))
    pg.display.set_caption("QR Code Generator")

    main_clock = pg.time.Clock()

    qr = qrcode.QRCode()
    qr_text = old_qr_text = image = None
    textbox_ = textbox.TextBox(window, 0, 100, 700, 50)
    textbox_.RECT.x = (window.get_width() - textbox_.RECT.width) // 2
    button_ = button.Button(window, "Generate QR Code", 0, 180, 250, 50)
    button_.RECT.x = (window.get_width() - button_.RECT.width) // 2

    title = "Enter URL below to convert it to QR Code"
    title_font = pg.font.SysFont("consolas", 30)
    title_to_display = title_font.render(title, True, pg.colordict.THECOLORS["blue"])
    title_x, title_y = (window.get_width() - title_to_display.get_width()) // 2, 40

    window_on = True

    while window_on:

        '''Taking Input'''

        textbox_.mouse_input()
        button_.mouse_input()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                window_on = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    window_on = False
                textbox_.keyboard_input(event)

        '''Processing'''

        if textbox_.action and textbox_.text != old_qr_text:
            old_qr_text, qr_text = qr_text, textbox_.text

        if button_.action and qr_text != old_qr_text:
            qr.clear()
            qr.add_data(qr_text)
            qr.make()
            image_ = qr.make_image()
            image_.save("QRCode.png")
            image = pg.image.load("QRCode.png")
            qr_text = ""

        '''Displaying'''

        window.fill(pg.colordict.THECOLORS["white"])

        window.blit(title_to_display, (title_x, title_y))
        button_.display()
        textbox_.display()
        if image:
            x = (window.get_width() - image.get_width()) // 2
            window.blit(image, (x, 250))

        pg.display.flip()

        main_clock.tick(60)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
