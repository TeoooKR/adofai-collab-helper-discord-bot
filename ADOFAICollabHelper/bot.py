import discord
from discord import app_commands
from dotenv import load_dotenv
import os
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()
bot = MyBot()
maps = {}
@bot.tree.command(name="map_add", description="곡을 추가합니다.")
@app_commands.describe(song_name="곡 이름", deadline="마감 기한")
async def add_map(interaction: discord.Interaction, song_name: str, deadline: str = None):
    maps[song_name] = {"deadline": deadline or "마감기한 없음", "parts": {}}
    await interaction.response.send_message(f"곡 '{song_name}'가 추가되었습니다. 마감기한: {deadline or '마감기한 없음'}")
@bot.tree.command(name="map_delete", description="곡을 삭제합니다.")
@app_commands.describe(song_name="곡 이름")
async def delete_map(interaction: discord.Interaction, song_name: str):
    if song_name in maps:
        del maps[song_name]
        await interaction.response.send_message(f"곡 '{song_name}'가 삭제되었습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="map_set", description="곡 정보를 수정합니다.")
@app_commands.describe(song_name="곡 이름", new_name="변경할 곡명", new_deadline="변경할 마감기한")
async def set_map(interaction: discord.Interaction, song_name: str, new_name: str, new_deadline: str = None):
    if song_name in maps:
        if new_name:
            maps[new_name] = maps.pop(song_name)
        if new_deadline:
            maps[new_name or song_name]["deadline"] = new_deadline
        await interaction.response.send_message(f"곡 '{song_name}'가 '{new_name or song_name}'로 변경되었습니다. 새 마감기한: {new_deadline or maps[new_name or song_name]['deadline']}")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="part_add", description="곡의 파트를 추가합니다.")
@app_commands.describe(song_name="곡 이름", part_name="파트 이름", start_time="시작 길이", end_time="끝 길이", deadline="마감 기한")
async def add_part(interaction: discord.Interaction, song_name: str, part_name: str = None, start_time: str = None, end_time: str = None, deadline: str = None):
    if song_name in maps:
        maps[song_name]["parts"][part_name] = {
            "start": start_time or "시작 길이 없음",
            "end": end_time or "끝 길이 없음",
            "deadline": deadline or "마감기한 없음",
            "editors": {}
        }
        await interaction.response.send_message(f"'{song_name}'에 '{part_name}'가 추가되었습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="part_delete", description="파트를 삭제합니다.")
@app_commands.describe(song_name="곡 이름", part_name="파트 이름")
async def delete_part(interaction: discord.Interaction, song_name: str, part_name: str):
    if song_name in maps and part_name in maps[song_name]["parts"]:
        del maps[song_name]["parts"][part_name]
        await interaction.response.send_message(f"'{song_name}'의 '{part_name}' 파트가 삭제되었습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}' 또는 파트 '{part_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="part_set", description="파트 정보를 수정합니다.")
@app_commands.describe(song_name="곡 이름", part_name="파트 이름", new_part_name="변경할 파트 이름", start_time="변경할 시작 길이", end_time="변경할 종료 길이", deadline="변경할 마감 기한")
async def set_part(interaction: discord.Interaction, song_name: str, part_name: str, new_part_name: str = None, start_time: str = None, end_time: str = None, deadline: str = None):
    if song_name in maps and part_name in maps[song_name]["parts"]:
        if new_part_name:
            maps[song_name]["parts"][new_part_name] = maps[song_name]["parts"].pop(part_name)
        if start_time:
            maps[song_name]["parts"][new_part_name or part_name]["start"] = start_time
        if end_time:
            maps[song_name]["parts"][new_part_name or part_name]["end"] = end_time
        if deadline:
            maps[song_name]["parts"][new_part_name or part_name]["deadline"] = deadline
        await interaction.response.send_message(f"'{song_name}'의 '{part_name}'가 '{new_part_name or part_name}'로 변경되었습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}' 또는 파트 '{part_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="editor_add", description="파트에 편집자를 추가합니다.")
@app_commands.describe(user="사용자", song_name="곡 이름", part_name="파트 이름", role="역할", display_name="표시할 이름")
async def add_editor(interaction: discord.Interaction, user: str, song_name: str, part_name: str = None, role: str = None, display_name: str = None):
    if song_name in maps:
        if part_name is None:            
            maps[song_name]["editors"] = maps[song_name].get("editors", {})
            maps[song_name]["editors"][user] = {"role": role or "역할 없음", "name": display_name or user}
            await interaction.response.send_message(f"'{user}'가 '{song_name}'에 추가되었습니다.")
        elif part_name in maps[song_name]["parts"]:            
            maps[song_name]["parts"][part_name]["editors"][user] = {"role": role or "역할 없음", "name": display_name or user}
            await interaction.response.send_message(f"'{user}'가 '{song_name}'의 '{part_name}'에 추가되었습니다.")
        else:
            await interaction.response.send_message(f"곡 '{song_name}'에는 '{part_name}' 파트가 없습니다. 파트를 지정해 주세요.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="editor_delete", description="파트에서 편집자를 삭제합니다.")
@app_commands.describe(user="사용자", song_name="곡 이름", part_name="파트 이름")
async def delete_editor(interaction: discord.Interaction, user: str, song_name: str, part_name: str = None):
    if song_name in maps:
        if part_name and part_name in maps[song_name]["parts"] and user in maps[song_name]["parts"][part_name]["editors"]:
            del maps[song_name]["parts"][part_name]["editors"][user]
            await interaction.response.send_message(f"'{user}'가 '{song_name}'의 '{part_name}'에서 삭제되었습니다.")
        elif user in maps[song_name]["editors"]:
            del maps[song_name]["editors"][user]
            await interaction.response.send_message(f"'{user}'가 '{song_name}'에서 삭제되었습니다.")
        else:
            await interaction.response.send_message(f"곡 '{song_name}' 또는 파트 '{part_name}'에서 '{user}'를 찾을 수 없습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="editor_set", description="편집자 정보를 수정합니다.")
@app_commands.describe(user="사용자", song_name="곡 이름", part_name="파트 이름", new_role="변경할 역할", new_display_name="변경할 표시 이름")
async def set_editor(interaction: discord.Interaction, user: str, song_name: str, part_name: str = None, new_role: str = None, new_display_name: str = None):
    if song_name in maps:
        if part_name and part_name in maps[song_name]["parts"] and user in maps[song_name]["parts"][part_name]["editors"]:
            if new_role:
                maps[song_name]["parts"][part_name]["editors"][user]["role"] = new_role
            if new_display_name:
                maps[song_name]["parts"][part_name]["editors"][user]["name"] = new_display_name
            await interaction.response.send_message(f"'{user}'의 편집자 정보가 '{part_name}'에서 업데이트되었습니다.")
        elif user in maps[song_name]["editors"]:
            if new_role:
                maps[song_name]["editors"][user]["role"] = new_role
            if new_display_name:
                maps[song_name]["editors"][user]["name"] = new_display_name
            await interaction.response.send_message(f"'{user}'의 편집자 정보가 '{song_name}'에서 업데이트되었습니다.")
        else:
            await interaction.response.send_message(f"곡 '{song_name}' 또는 파트 '{part_name}'에서 '{user}'를 찾을 수 없습니다.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="progress", description="파트의 진행 상황을 추가/수정합니다.")
@app_commands.describe(song_name="곡 이름", part_name="파트 이름", progress_status="진행 상태")
async def progress(interaction: discord.Interaction, song_name: str, part_name: str = None, progress_status: str = None):
    if song_name in maps:
        if part_name:
            if part_name in maps[song_name]["parts"]:
                if progress_status:
                    maps[song_name]["parts"][part_name]["progress"] = progress_status
                    await interaction.response.send_message(f"'{song_name}'의 '{part_name}' 파트 진행 상황이 '{progress_status}'로 업데이트되었습니다.")
                else:
                    await interaction.response.send_message("진행 상태를 입력해 주세요.")
            else:
                await interaction.response.send_message(f"곡 '{song_name}'에 '{part_name}' 파트를 찾을 수 없습니다.")
        else:
            if progress_status:
                maps[song_name]["progress"] = progress_status
                await interaction.response.send_message(f"'{song_name}'의 전체 곡 진행 상황이 '{progress_status}'로 업데이트되었습니다.")
            else:
                await interaction.response.send_message("진행 상태를 입력해 주세요.")
    else:
        await interaction.response.send_message(f"곡 '{song_name}'를 찾을 수 없습니다.")
@bot.tree.command(name="list", description="등록된 곡 및 파트 목록을 보여줍니다.")
async def list_maps(interaction: discord.Interaction):
    if not maps:
        await interaction.response.send_message("등록된 곡이 없습니다.")
    else:
        response = []
        for song, data in maps.items():            
            song_info = f"# {song} (마감: {data['deadline']})"
            parts_info = []
            for part, part_data in data["parts"].items():                
                part_info = f"- {part} ({part_data['start']}~{part_data['end']}) (마감: {part_data['deadline']})"
                editors_info = "\n".join([f"  - {editor_data['role']}: {editor_data['name']} @{editor}" 
                                          for editor, editor_data in part_data.get('editors', {}).items()])
                progress_info = f"- 상태: `{part_data.get('progress', '상태 없음')}`"
                parts_info.append(part_info + "\n" + editors_info + "\n" + progress_info)            
            if not parts_info:
                editors_info = "\n".join([f"- {editor_data['role']}: {editor_data['name']} @{editor}"
                                          for editor, editor_data in data.get('editors', {}).items()])
                parts_info.append(editors_info)           
            response.append(song_info + "\n" + "\n".join(parts_info))
        await interaction.response.send_message("\n\n".join(response))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(DISCORD_TOKEN)