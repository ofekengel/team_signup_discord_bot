import re
from typing import List

from model.leagues import LEAGUES
from model.team import Team
from parsers.bot_command_parser import BotCommandParser, CommandParserException
from model.captain import Captain
from commands.store_team import StoreTeam
from model.role_enum import RoleEnum
from model.team_member import TeamMember


class CouldNotParseTeamException(Exception):
    pass


class CouldNotFindTeamNameException(Exception):
    pass


class CouldNotFindCaptainNameException(Exception):
    pass


# todo: name regex vars
class LeagueNameParseException(Exception):
    pass


class SignCommandParser(BotCommandParser):
    # todo: get Message and use author_response.raw_mentions[0] to get ids and not regex
    @classmethod
    def parse(cls, raw_message: str) -> StoreTeam:
        try:
            command_lines = raw_message.split('\n')
            team = command_lines[0]
            league = command_lines[1]
            members = command_lines[2:]

            players = []
            captain = ''
            team_tag = cls.__get_team_tag(team)
            team_name = team.replace(team_tag, '')[:-1]

            for member in members:
                name = cls.__get_id(re.search(r'<@[!&][^><]+>', member).group())
                role = cls.__get_role(member)
                profile_link = cls.__get_profile_link(member)
                if role == RoleEnum.CAPTAIN.value:
                    captain = Captain(name, team_name, profile_link)
                else:
                    players.append(TeamMember(name, team_name, profile_link))

            league_name = cls.__get_league_name(league)
            if captain != '':
                signed_team = StoreTeam(Team(team_name, league_name, team_tag), captain, players)
            else:
                raise CommandParserException('Please enter a team captain')

            return signed_team
        except CouldNotFindTeamNameException:
            raise CommandParserException('Please enter team name right')
        except CouldNotFindCaptainNameException:
            raise CommandParserException('Please enter captain name right')
        except LeagueNameParseException:
            raise CommandParserException('Please enter league name right')

    @staticmethod
    def __get_role(message: str) -> str:
        return re.search(r'role: \w+', message).group().split(' ')[1]

    @staticmethod
    def __get_profile_link(message: str) -> str:
        return re.search(r'[^ ]+$', message).group()

    @staticmethod
    def __get_id(message: str) -> str:
        return re.search(r'\d+', message).group()

    @classmethod
    def __get_league_name(cls, message: str) -> str:
        role = re.search(r': [^,]+', message).group()[2:]
        if role.strip() not in LEAGUES.keys():
            raise LeagueNameParseException()
        return role

    @classmethod
    def __get_team_tag(cls, message: str) -> str:
        return re.search(r'\[.+\]', message).group()
