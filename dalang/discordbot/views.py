import discord


class ButtonView(discord.ui.View):
    @discord.ui.button(
        label="Vibe!", style=discord.ButtonStyle.primary, emoji="😎"
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        # await bot.invoke(bot.get_command("recommend"))
        await interaction.response.send_message("You clicked the button!")


class MoodSelectView(discord.ui.View):
    @discord.ui.select(  # the decorator that lets you specify the properties of the select menu
        placeholder="Choose a Flavor!",  # the placeholder text that will be displayed if nothing is selected
        min_values=1,  # the minimum number of values that must be selected by the users
        max_values=1,  # the maxmimum number of values that can be selected by the users
        options=[  # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla", description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!",
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!",
            ),
        ],
    )
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        await interaction.response.send_message(
            f"Awesome! I like {select.values[0]} too!"
        )
