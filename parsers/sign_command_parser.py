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


class NoTeamTagException(Exception):
    pass


class MentionParseException(Exception):
    pass


class NoIdException(Exception):
    pass


class NoRoleException(Exception):
    pass


class URLNotFoundException(Exception):
    pass


class BadUrlFormatException(Exception):
    pass


class WrongLinkException(Exception):
    pass


class SignCommandParser(BotCommandParser):
    # todo: get Message and use author_response.raw_mentions[0] to get ids and not regex
    @classmethod
    def parse(cls, raw_message: str) -> StoreTeam:
        print('parsing sign')
        try:
            command_lines = cls.__get_rows(raw_message)
            team = command_lines[0]
            league = command_lines[1]
            members = command_lines[2:]

            players = []
            captain = ''
            team_tag = cls.__get_team_tag(team)
            team_name = team.replace(team_tag, '')[:-1]

            for member in members:
                name = cls.__get_id(cls.__get_mention(member))
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
        except NoTeamTagException:
            raise CommandParserException('Please enter team tag right')
        except MentionParseException:
            raise CommandParserException(
                'Please make sure mentioned players appear in blue, links are in the same row as player and picture is a file and not a link')
        except NoRoleException:
            raise CommandParserException('Please make sure you enter roles as shown in the example')
        except WrongLinkException:
            raise CommandParserException('Please make sure you use an r6stats link')
        except BadUrlFormatException:
            raise CommandParserException('Please make sure you are using an https://r6stats.com/stats/ link')
        except URLNotFoundException:
            raise CommandParserException('Please enter a link to you r6stats profile')

    @staticmethod
    def __get_mention(message: str) -> str:
        mention = re.search(r'<@[^><]+>', message)
        if mention is None:
            raise MentionParseException()

        return mention.group()

    @staticmethod
    def __get_role(message: str) -> str:
        try:
            return re.search(r'role: \w+', message).group().split(' ')[1]
        except AttributeError:
            raise NoRoleException()

    @staticmethod
    def __get_profile_link(message: str) -> str:
        url = re.search(r'[^ ]+$', message.strip()).group()
        if url is not None:
            if 'https' in url:
                # if 'r6stats' not in url:
                return url
                # raise WrongLinkException()
            raise BadUrlFormatException()
        raise URLNotFoundException()

    @staticmethod
    def __get_id(message: str) -> str:
        try:
            return re.search(r'\d+', message).group()
        except AttributeError:
            raise NoIdException()

    @classmethod
    def __get_league_name(cls, message: str) -> str:
        role = re.search(r': [^,]+', message).group()[2:]
        if role.strip() not in LEAGUES.keys():
            raise LeagueNameParseException()
        return role

    @classmethod
    def __get_team_tag(cls, message: str) -> str:
        try:
            return re.search(r'\[.+\]', message).group()
        except AttributeError:
            raise NoTeamTagException()

    @classmethod
    def __get_rows(cls, raw_message: str) -> List[str]:
        rows = raw_message.split('\n')
        good_rows = []
        for row in rows:
            if len(row) > 1:
                good_rows.append(row)
        return good_rows
