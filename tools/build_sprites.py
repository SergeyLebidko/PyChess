"""Сборка PNG-спрайтов фигур из SVG-набора Cburnett (Wikimedia Commons).

Скрипт не входит в игру и запускается только при разработке. Он скачивает
каноничные шахматные фигуры (набор Cburnett, лицензия CC BY-SA) и конвертирует
их в PNG нужного размера, перезаписывая файлы в game_pack/sprites/.

Рантайм игры не зависит от этого скрипта и от cairosvg: в репозиторий
попадают уже сгенерированные PNG.

Запуск (из корня проекта):
    pip install -r tools/requirements-build.txt
    python tools/build_sprites.py
"""
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_pack.params import CELL_SIZE

try:
    import cairosvg
except ImportError:
    sys.exit("Не найден cairosvg. Установите: pip install -r tools/requirements-build.txt")

# Исходное разрешение рендера: в два раза больше клетки, чтобы фигуры
# оставались резкими при масштабировании в игре.
RENDER_SCALE = 2

# Соответствие: имя файла Commons -> имя файла в game_pack/sprites
SPRITES = {
    'Chess_klt45.svg': 'whiteKing.png',
    'Chess_qlt45.svg': 'whiteQueen.png',
    'Chess_rlt45.svg': 'whiteRook.png',
    'Chess_blt45.svg': 'whiteBishop.png',
    'Chess_nlt45.svg': 'whiteKnight.png',
    'Chess_plt45.svg': 'whitePawn.png',
    'Chess_kdt45.svg': 'blackKing.png',
    'Chess_qdt45.svg': 'blackQueen.png',
    'Chess_rdt45.svg': 'blackRook.png',
    'Chess_bdt45.svg': 'blackBishop.png',
    'Chess_ndt45.svg': 'blackKnight.png',
    'Chess_pdt45.svg': 'blackPawn.png',
}

SOURCE_URL = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
USER_AGENT = 'PyChess-build-script/1.0 (sprite builder; contact: local)'

SPRITES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'game_pack', 'sprites')


def download_svg(name, attempts=6):
    url = SOURCE_URL + name
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
            if b'<svg' not in data[:2000]:
                raise RuntimeError("Не удалось получить SVG: %s" % url)
            return data
        except urllib.error.HTTPError as error:
            # Сервер может ограничивать частоту запросов, повторяем с паузой
            if error.code in (429, 503) and attempt < attempts - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise RuntimeError("Не удалось скачать SVG: %s" % url)


def main():
    size = CELL_SIZE * RENDER_SCALE
    os.makedirs(SPRITES_DIR, exist_ok=True)

    for index, (source_name, target_name) in enumerate(SPRITES.items()):
        if index:
            # Небольшая пауза между запросами, чтобы не попасть под
            # ограничение частоты обращений Wikimedia.
            time.sleep(1)
        svg_data = download_svg(source_name)
        png_data = cairosvg.svg2png(bytestring=svg_data, output_width=size, output_height=size)
        target_path = os.path.join(SPRITES_DIR, target_name)
        with open(target_path, 'wb') as target_file:
            target_file.write(png_data)
        print("%s -> %s (%dx%d)" % (source_name, target_name, size, size))

    print("Готово. Спрайты размером %dx%d записаны в %s" % (size, size, SPRITES_DIR))


if __name__ == '__main__':
    main()
