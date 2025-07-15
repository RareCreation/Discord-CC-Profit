import os

import disnake
from disnake.ext import commands
from config.config import moderation_role_id

from PIL import Image, ImageDraw, ImageFont
import io

from paths.paths import background_path, second_background_path, font_path, countries_path


class LogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="")
    async def log(
            self,
            inter: disnake.ApplicationCommandInteraction,
            worker: str,
            dobiver: str,
            profit: str,
            geo: str = commands.Param(choices=["EU", "CHINA", "USA"]),
            wechat: str = None
    ):

        if not any(role.id in moderation_role_id for role in inter.author.roles):
            await inter.response.send_message("У вас нет доступа к этой команде.", ephemeral=True)
            return

        if wechat:
            image = Image.open(second_background_path).convert("RGB")
            positions = {
                "worker": 630,
                "dobiver": 822,
                "wechat": 1012,
                "geo": 1180,

            }
        else:
            image = Image.open(background_path).convert("RGB")
            positions = {
                "worker": 750,
                "dobiver": 970,
                "geo": 1155,
            }

        draw = ImageDraw.Draw(image)
        main_font = ImageFont.truetype(font_path, size=40)
        font_profit = ImageFont.truetype(font_path, size=120)

        def draw_centered_text(text, center_x, y, font_obj, fill):
            text_width = draw.textlength(text, font=font_obj)
            draw.text((center_x - text_width / 2, y), text, font=font_obj, fill=fill)



        draw_centered_text(worker, positions["worker"], 280, main_font, (255, 255, 255))
        draw_centered_text(dobiver, positions["dobiver"], 280, main_font, (255, 255, 255))
        draw_centered_text(f"{profit}$", 1020, 385, font_profit, (255, 255, 255))

        if wechat:
            draw_centered_text(wechat, positions["wechat"], 280, main_font, (255, 255, 255))

        geo_icon_path = countries_path.get(geo.upper())
        if geo_icon_path and os.path.exists(geo_icon_path):
            geo_icon = Image.open(geo_icon_path).convert("RGBA")
            geo_icon = geo_icon.resize((50, 50))
            image.paste(geo_icon, (positions["geo"] - 40, 270), geo_icon)


        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        file = disnake.File(buffer, filename="log.jpg")
        await inter.response.send_message(content="@everyone", file=file, ephemeral=False, allowed_mentions=disnake.AllowedMentions(everyone=True))


def setup(bot):
    bot.add_cog(LogCog(bot))
