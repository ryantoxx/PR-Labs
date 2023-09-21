from player import Player
import player_pb2
import player_pb2 as PlayersList
from datetime import datetime
import xml.etree.ElementTree as ET

class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        player_json = []
        for player in players:
            player_dict = {
                "nickname": player.nickname,
                "email": player.email,
                "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                "xp": player.xp,
                "class": player.cls,
            }
            player_json.append(player_dict)
        return player_json

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        player_list = []

        for player in list_of_dict:
            nickname = player["nickname"]
            email = player["email"]
            date_of_birth = player["date_of_birth"]
            xp = player["xp"]
            cls = player["class"]
            player_list.append(Player(nickname, email, date_of_birth, xp, cls))

        return player_list

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        players = []
        root = ET.fromstring(xml_string)
        for player_element in root.findall("player"):
            nickname = player_element.find("nickname").text
            email = player_element.find("email").text
            date_of_birth_str = player_element.find("date_of_birth").text  
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d")  
            xp = int(player_element.find("xp").text)
            player_class = player_element.find("class").text

            player = Player(nickname, email, date_of_birth.strftime("%Y-%m-%d"), xp, player_class)
            players.append(player)
        return players

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        root = ET.Element("data")
        for player in list_of_players:
            player_element = ET.SubElement(root, "player")
            ET.SubElement(player_element, "nickname").text = player.nickname
            ET.SubElement(player_element, "email").text = player.email
            ET.SubElement(player_element, "date_of_birth").text = player.date_of_birth.strftime("%Y-%m-%d")
            ET.SubElement(player_element, "xp").text = str(player.xp)
            ET.SubElement(player_element, "class").text = player.cls

        xml_string = ET.tostring(root, encoding="utf-8")
        return xml_string.decode("utf-8")

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        players_list = player_pb2.PlayersList()
        players_list.ParseFromString(binary)
        players = []
            
        for player_item in players_list.player:
            player = Player(
                player_item.nickname,
                player_item.email,
                player_item.date_of_birth,
                player_item.xp,
                player_pb2.Class.Name(player_item.cls),
            )
            players.append(player)
        return players

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        player_data = PlayersList.PlayersList()
        
        for players in list_of_players:
            player_item = player_data.player.add()
            player_item.nickname = players.nickname
            player_item.email = players.email
            player_item.date_of_birth = players.date_of_birth.strftime("%Y-%m-%d")
            player_item.xp = players.xp
            player_item.cls = players.cls
        
        result = player_data.SerializeToString()
        return result
            

