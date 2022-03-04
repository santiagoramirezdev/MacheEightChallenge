import requests
import unittest


def get_json_data():
    """
    this method call the api and return a json with NBA players
    :return: r
    """
    r = requests.get('https://mach-eight.uc.r.appspot.com')
    return r.json()


def get_name(player):
    """
    this method allow get the name of a player

    :param player: dictionary with a player
    :return: name of a player dict, frist name follow by last name
    """
    first_name = player['first_name']
    last_name = player['last_name']
    name = f'{first_name} {last_name} '
    return name


def show_pairs(matching_pairs_list, player):
    """
    Returns a message with the pairs, who´s combined height is the desired height
    :param matching_pairs_list: list of matching pair who´s combined height is the desired height
    :param player: the player that we are evaluating
    :return:   string
    """
    message = ''
    player_name = get_name(player)
    for players in matching_pairs_list:
        if player_name != get_name(players):
            message = message + f'{player_name} ---> {get_name(players)}   \n'

    return message


def finding_pairs(value):
    """
    Calls an API to obtain the list of players, then it orders it by players height in ascending order,
    Then it iterates over each player, and using binary search it looks for players who´s height when added
    up, return the desired height. In case there isn´t there isn´t any height left who matches the expected value
    it breaks from loop.
    :cost: n/2*Log(n)
    :param value: desireed height
    :return:  message
    """
    json = get_json_data()
    list_of_players = json['values']
    sorted_list_of_players = sorted(list_of_players, key=lambda d: d['h_in'])
    message = ''
    minimun_height = int(sorted_list_of_players[0]['h_in'])
    for player in sorted_list_of_players:
        h_in = int(player['h_in'])

        left_to_value = value - h_in
        if left_to_value < minimun_height:
            break
        index = binary_search(sorted_list_of_players, left_to_value, 0, len(sorted_list_of_players) - 1)
        if index != -1:
            matching_pairs_list = matching_pairs(sorted_list_of_players, index)
            message = message + show_pairs(matching_pairs_list, player)

        player['h_in']=0
    if message == '':
        message = f'there is not match'

    return message


def binary_search(sorted_list_of_players, target, left, right):
    """
     Binary search
    :param sorted_list_of_players: list of players sorted by height
    :param target: value whos sum with another height will match expected height
    :param left: indicates left most player
    :param right: indicates right most player
    :return: the index where the desired height is located
    """
    if left > right:
        return -1

    mid = (left + right) // 2
    if target == int(sorted_list_of_players[mid]['h_in']):
        return mid
    elif target < int(sorted_list_of_players[mid]['h_in']):
        return binary_search(sorted_list_of_players, target, left, mid - 1)
    else:
        return binary_search(sorted_list_of_players, target, mid + 1, right)


def matching_pairs(sorted_list_of_players, index):
    """
    Creates a list with all the possible matches for a player, it will select the neighbors
    of the index value, found by the binary search, who´s heights are the same as the player in the index.
    :param sorted_list_of_players: list of players sorted by height
    :param index: the index where the desired height is
    :return: list with all the possible pairs
    """
    matching_pairs_list = []
    matching_pairs_list.append(sorted_list_of_players[index])
    target = sorted_list_of_players[index]['h_in']
    counter = 1
    try:
        while sorted_list_of_players[index + counter]['h_in'] == target or sorted_list_of_players[index - counter][
            'h_in'] == target:
            if sorted_list_of_players[index + counter]['h_in'] == target:
                matching_pairs_list.append(sorted_list_of_players[index + counter])
            if sorted_list_of_players[index - counter]['h_in'] == target:
                matching_pairs_list.append(sorted_list_of_players[index - counter])


            counter += 1
        return matching_pairs_list
    except:
        return matching_pairs_list


class test_finding_pairs(unittest.TestCase):

    def test_example_case(self):

        """the case of the challenge"""
        message = 'Nate Robinson  ---> Mike Wilks    \nNate Robinson  ---> Brevin Knight    \n'
        self.assertEqual(finding_pairs(139), message)

    def test_case_lowest_posible(self):
        """Tests the minimum height"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(138), message)

    def test_case_lowest_imposible(self):
        """Tests a value which can obtain due to it being too small"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(137), message)

    def test_case_maximum_two_diffent_players(self):
        """Test two tallest players"""
        message = 'Zydrunas Ilgauskas  ---> Yao Ming    \n'
        self.assertEqual(finding_pairs(177), message)

    def test_case_maximum_posible(self):
        """Tests the maximum height"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(180), message)

    def test_case_maximum_imposible(self):
        """Tests a value which can obtain due to it being too big"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(181), message)

    def test_case_cero(self):
        """Test when the desired height is 0"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(0), message)

    def test_case_negative(self):
        """Test when the desired height is a negative number"""
        message = 'there is not match'
        self.assertEqual(finding_pairs(-1), message)


if __name__ == '__main__':

    # Example of challenge
    message = finding_pairs(139)
    print(f'The example of challenge \n{message}')
    # Exapmple that i use to work
    message = finding_pairs(152)
    print(f'Exapmple that i use to work \n{message}')
    # tests
    print(f'unit testing, consist in 9 cases: ')

    suite = unittest.TestLoader().loadTestsFromTestCase(test_finding_pairs)
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)