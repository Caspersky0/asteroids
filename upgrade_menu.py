
import pygame

from upgrades import UPGRADES


def draw_upgrade_menu(screen, font, choices):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(
        "assets/fonts/PressStart2P-regular.ttf",
        26,
    )

    title = title_font.render("LEVEL UP!", True, (100, 255, 150))
    title_rect = title.get_rect(
        center=(screen.get_width() / 2, 150)
    )
    screen.blit(title, title_rect)

    subtitle = font.render("Choose an upgrade", True, "white")
    subtitle_rect = subtitle.get_rect(
        center=(screen.get_width() / 2, 205)
    )
    screen.blit(subtitle, subtitle_rect)

    card_width = 420
    card_height = 180
    gap = 30

    total_width = card_width * 2 + gap
    start_x = (screen.get_width() - total_width) / 2
    y = 290

    rects = []

    for index, key in enumerate(choices):
        x = start_x + index * (card_width + gap)
        rect = pygame.Rect(x, y, card_width, card_height)

        pygame.draw.rect(
            screen,
            (25, 35, 55),
            rect,
            border_radius=12,
        )
        pygame.draw.rect(
            screen,
            (100, 220, 255),
            rect,
            3,
            border_radius=12,
        )

        name = title_font.render(
            UPGRADES[key]["name"],
            True,
            "white",
        )
        name_rect = name.get_rect(
            center=(rect.centerx, rect.y + 55)
        )
        screen.blit(name, name_rect)

        description = UPGRADES[key]["description"]
        words = description.split()
        lines = []
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()

            if font.size(test_line)[0] > card_width - 40:
                if line:
                    lines.append(line)
                line = word
            else:
                line = test_line

        if line:
            lines.append(line)

        for line_index, text in enumerate(lines):
            surface = font.render(
                text,
                True,
                (200, 210, 225),
            )
            text_rect = surface.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 105 + line_index * 30,
                )
            )
            screen.blit(surface, text_rect)

        rects.append((rect, key))

    return rects
