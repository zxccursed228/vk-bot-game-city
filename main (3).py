import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from lobby import Lobby
from cities_list import cities_list
import secret_constants

vk_session = vk_api.VkApi(token=secret_constants.TOKEN)
longpoll = VkLongPoll(vk_session)


def is_message(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me


def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})


def get_user_name(user_id):
    user_info = vk_session.method('users.get',
                                  {'user_ids': [user_id]})
    if len(user_info) > 0:
        return user_info[0]['first_name'] + ' ' + user_info[0]['last_name']


def is_start_game(event):
    start_commands = ['играть в города', "хочу играть в города", "города",
                      'Играть в города', "Хочу играть в города", "Города"]
    return event.text.lower() in start_commands


def find_lobby(lobbies, user_id):
    for lobby in lobbies:
        if user_id in lobby.user_ids:
            return lobby

def main():
    players_queue = None
    lobbies = []
    users_in_game = []
    for event in longpoll.listen():
        if is_message(event):
            if event.text == 'привет':
                send_message(event.user_id, 'Привет!')
            elif is_start_game(event):
                if players_queue is None:
                    send_message(event.user_id, 'вы в очереди')
                    players_queue = event.user_id
                elif event.user_id != players_queue:
                    user1 = players_queue
                    user2 = event.user_id
                    lobbies.append(Lobby(user1, user2))
                    users_in_game.extend((user1, user2))
                    players_queue = None
                    send_message(user1, 'Игра началась!')
                    send_message(user2, 'Игра началась!')
                    send_message(lobbies[-1].get_active_player_id(), 'вы ходите первым, наховите город на любую букву')
                    send_message(lobbies[-1].get_inactive_player_id(), 'ваш соперник ходит первым')
            elif event.user_id in users_in_game:
                city = event.text.lower()
                lobby = find_lobby(lobbies, event.user_id)
                if city not in cities_list:
                    send_message(event.user_id, 'Такого города нет, либо же проверь на опечатку \n'
                                 'Ты проиграл')
                    send_message(lobby.get_inactive_player_id(), 'ты победил!')
                    users_in_game.remove(event.user_id)
                    users_in_game.remove(lobby.get_inactive_player_id())
                    lobbies.remove(lobby)
                    continue
                elif not lobby.is_correct_letter(city[0].lower()):
                    send_message(event.user_id, 'Не та буква даун.... купи букваръ! учи геаграфию')
                    continue
                elif lobby.get_active_player_id() != event.user_id:
                    send_message(event.user_id, 'завали ебло, не твой ход')
                    continue

                lobby.change_ll(city)
                lobby.used_cities.append(city)
                lobby.change_cur_turn()
                send_message(lobby.get_active_player_id(), f'Вам на букву: {lobby.last_letter}.\n'
                                                           f'Игрок назвал город: {city}')


main()
