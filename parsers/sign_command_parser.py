import re
from typing import List

from parsers.bot_command_parser import BotCommandParser
from team_members.captain import Captain
from commands.store_team import StoreTeam
from team_members.team_member import TeamMember


class CouldNotParseTeamException(Exception):
    pass


class CouldNotFindTeamNameException(Exception):
    pass


class CouldNotFindCaptainNameException(Exception):
    pass


# todo: name regex vars
class SignCommandParser(BotCommandParser):
    @classmethod
    def parse(cls, raw_message: str) -> StoreTeam:
        try:
            captain_name = cls.__find_captain(raw_message)
            team_members = cls.__find_team_members_names(raw_message)
            team_name = cls.__find_team_name(raw_message)

            captain = Captain(captain_name, team_name)
            players = []
            for member in team_members:
                players.append(TeamMember(member, team_name))

            team = StoreTeam(team_name, captain, players)

            return team
        except CouldNotFindTeamNameException as e:
            raise e
        except CouldNotFindCaptainNameException as e:
            raise e

    @staticmethod
    def __find_captain(message: str) -> str:
        captain_info_section = re.search(r'<@[!&][^><]+> as captain', message)
        if captain_info_section is not None:
            return re.search(r'<@[!&][^><]+>', captain_info_section.group()).group()
        raise CouldNotFindCaptainNameException()

    @staticmethod
    def __find_team_members_names(message: str) -> List[str]:
        members_info_section = re.search('members: (<@!.*>, ){0,7}(<@!.*>)', message)
        if members_info_section is not None:
            return re.findall('<@[!&][^><]+>', members_info_section.group())
        return []

    @staticmethod
    def __find_team_name(message: str) -> str:
        # i have removed escaped space from regex
        team_name_section = re.search(r'for team .*', message)
        if team_name_section is not None:
            team_name = re.search('[^ ]+$', team_name_section.group())
            if team_name is not None:
                return team_name.group()
        raise CouldNotFindTeamNameException()
