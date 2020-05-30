import re
from typing import List
from parsers.bot_command_parser import BotCommandParser, CommandParserException
from team_members.captain import Captain
from commands.store_team import StoreTeam
from team_members.role_enum import RoleEnum
from team_members.team_member import TeamMember


class CouldNotParseTeamException(Exception):
    pass


class CouldNotFindTeamNameException(Exception):
    pass


class CouldNotFindCaptainNameException(Exception):
    pass


# todo: name regex vars
class SignCommandParser(BotCommandParser):
    # todo: get Message and use author_response.raw_mentions[0] to get ids and not regex
    @classmethod
    def parse(cls, raw_message: str) -> StoreTeam:
        try:
            command_lines = raw_message.split('\n')
            team_name = command_lines[0]
            members = command_lines[1:]
            players = []
            captain = ''
            for member in members:
                name = cls.__get_id(re.search(r'<@[!&][^><]+>', member).group())
                role = cls.__get_role(member)
                profile_link = cls.__get_profile_link(member)
                if role == RoleEnum.CAPTAIN.value:
                    captain = Captain(name, team_name, profile_link)
                else:
                    players.append(TeamMember(name, team_name, profile_link))
            if captain != '':
                team = StoreTeam(team_name, captain, players)
            else:
                raise CommandParserException('Please enter a team captain')

            return team
        except CouldNotFindTeamNameException:
            raise CommandParserException('Please enter team name right')
        except CouldNotFindCaptainNameException:
            raise CommandParserException('Please enter captain name right')

    @staticmethod
    def __get_role(message: str) -> str:
        return re.search('role: \w+', message).group().split(' ')[1]

    @staticmethod
    def __get_profile_link(message: str) -> str:
        return re.search('[^ ]+$', message).group()


    @staticmethod
    def __get_id(message: str) -> str:
        return re.search(r'\d+', message).group()
