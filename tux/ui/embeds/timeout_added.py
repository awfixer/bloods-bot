embed = discord.Embed(colour=0x00B0F4, timestamp=datetime.now())

embed.set_author(
    name="Case 50 - Timeout Added (60m)",
    icon_url="https://github.com/allthingslinux/tux/blob/main/assets/slicedsymbol-0.png?raw=true",
)

embed.add_field(name="Moderator", value="__kzndotsh__\n`1172803065779339304`", inline=True)
embed.add_field(name="Member", value="__someverylongusername__\n`548410451818708993`", inline=True)
embed.add_field(name="Reason", value="> dasdjhasdkjahsdkjhasdkjhs", inline=False)

embed.set_footer(text="kzndotsh@atl $ 20.9ms")

await ctx.send(embed=embed)


{
    "author": {
        "name": "Case 50 - Timeout Added (60m)",
        "icon_url": "https://github.com/allthingslinux/tux/blob/main/assets/slicedsymbol-0.png?raw=true",
    },
    "fields": [
        {"name": "Moderator", "value": "__kzndotsh__\n`1172803065779339304`", "inline": true},
        {
            "name": "Member",
            "value": "__someverylongusername__\n`548410451818708993`",
            "inline": true,
        },
        {"name": "Reason", "value": "> dasdjhasdkjahsdkjhasdkjhs"},
    ],
    "color": "#00b0f4",
    "footer": {"text": "kzndotsh@atl $ 20.9ms"},
    "timestamp": 1718917690276,
}
