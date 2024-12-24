async def log_join(original_invites, vanity_invite, member):
    new_invites = await member.guild.invites()
    try:
        new_vanity = await member.guild.vanity_invite()
    except:
        new_vanity = None

    log_channel = next(filter(lambda channel: channel.name == 'invites', member.guild.channels))

    used_invite = next(filter(lambda invite: invite.uses > original_invites.get(invite.code), new_invites))
    if not used_invite:
        if new_vanity and new_vanity.uses > vanity_invite.get('uses'):
            used_invite = new_vanity
            vanity_invite['uses'] = vanity_invite.get('uses') + 1
    else:
        original_invites[used_invite.code] = original_invites.get(used_invite.code) + 1
    if not used_invite:
        await log_channel.send(f"<@{member.id}> joined but I couldn't find through which invite.")
        return

    await log_channel.send(f"<@{member.id}> joined using invite code `{used_invite.code}` from `{used_invite.inviter.name}`. Code has been used `{used_invite.uses}` times since creation.")


async def log_leave(member):
    log_channel = next(filter(lambda channel: channel.name == 'invites', member.guild.channels))
    await log_channel.send(f"<@{member.id}> has left the server")
