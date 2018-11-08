#coding: utf-8

import math
import re

class Move:
    def __init__(self, markers, all_markers):
        self.markers = markers
        self.all_markers = all_markers
        #Left bottom: <Vector (-3.6412, 3.6616, 0.3728)>
        #Right bottom: <Vector (-3.6503, -3.6722, 0.3728)>
        #Right top: <Vector (3.6801, -3.6722, 0.3728)>
        #Left top: <Vector (3.6795, 3.6616, 0.3728)>

        self.Z = 0.37
        self.top_X_border = 3.68
        self.bot_X_border = -3.65
        self.right_Y_border = -3.67
        self.left_Y_border = 3.66

        self.X_step = round(math.fabs((self.right_Y_border - self.left_Y_border) / 12), 2)
        self.Y_step = round(math.fabs((self.top_X_border - self.bot_X_border) / 12), 2)
        print(self.X_step, self.Y_step)
        self.wc_coord = {1: {'bot': [self.bot_X_border + self.X_step, self.left_Y_border - 3 * self.Y_step, self.Z],
                             'left': [self.top_X_border - 3 * self.X_step, self.left_Y_border - self.Y_step, self.Z],
                             'top': [self.top_X_border - self.X_step, self.right_Y_border + 3 * self.Y_step, self.Z],
                             'right': [self.bot_X_border + 3 * self.X_step, self.right_Y_border + self.Y_step, self.Z]},
                         3: {'bot': [self.bot_X_border + self.X_step, self.left_Y_border - 2 * self.Y_step, self.Z],
                             'left': [self.top_X_border - 2 * self.X_step, self.left_Y_border - self.Y_step, self.Z],
                             'top': [self.top_X_border - self.X_step, self.right_Y_border + 2 * self.Y_step, self.Z],
                             'right': [self.bot_X_border + 2 * self.X_step, self.right_Y_border + self.Y_step, self.Z]},
                         6: {'bot': [self.bot_X_border + self.X_step, self.left_Y_border - self.Y_step, self.Z],
                             'left': [self.top_X_border - self.X_step, self.left_Y_border - self.Y_step, self.Z],
                             'top': [self.top_X_border - self.X_step, self.right_Y_border + self.Y_step, self.Z],
                             'right': [self.bot_X_border + self.X_step, self.right_Y_border + self.Y_step, self.Z]}}

        self.marker_in_wc = {1: [], 3: [], 6: []}

        self.marker_start = {'Green': [self.bot_X_border, round(self.right_Y_border + self.left_Y_border, 2), self.Z],
                             'Yellow': [round(self.top_X_border + self.bot_X_border, 2), self.left_Y_border, self.Z],
                             'Blue': [self.top_X_border, round(self.right_Y_border + self.left_Y_border, 2), self.Z],
                             'Red': [round(self.top_X_border + self.bot_X_border, 2), self.right_Y_border, self.Z]}

        # self.wc_input = {'bot': [self.bot_X_border, round((self.right_Y_border + self.left_Y_border) + 3 * self.Y_step, 2), self.Z],
        #                  'left': [round((self.top_X_border + self.bot_X_border) + 3 * self.X_step, 2), self.left_Y_border, self.Z],
        #                  'top': [self.top_X_border, round((self.right_Y_border + self.left_Y_border) - 3 * self.Y_step, 2), self.Z],
        #                  'right': [round((self.top_X_border + self.bot_X_border) - 3 * self.X_step, 2), self.right_Y_border, self.Z]}

        self.wc_input = {'bot': [self.bot_X_border, round(self.left_Y_border - 3 * self.Y_step, 2), self.Z],
                         'left': [round(self.top_X_border - 3 * self.X_step, 2), self.left_Y_border, self.Z],
                         'top': [self.top_X_border, round(self.right_Y_border + 3 * self.Y_step, 2), self.Z],
                         'right': [round(self.bot_X_border + 3 * self.X_step, 2), self.right_Y_border, self.Z]}

        self.stairs = {'left_bot_up': [self.bot_X_border, self.left_Y_border - 4 * self.Y_step, self.Z],
                       'left_bot_down': [self.bot_X_border + 4 * self.X_step, self.left_Y_border, self.Z],
                       'left_top_up': [self.top_X_border - 4 * self.X_step, self.left_Y_border, self.Z],
                       'left_top_down': [self.top_X_border, self.left_Y_border - 4 * self.Y_step, self.Z],
                       'right_top_up': [self.top_X_border, self.right_Y_border + 4 * self.Y_step, self.Z],
                       'right_top_down': [self.top_X_border - 4 * self.X_step, self.right_Y_border, self.Z],
                       'right_bot_up': [self.bot_X_border + 4 * self.X_step, self.right_Y_border, self.Z],
                       'right_bot_down': [self.bot_X_border, self.right_Y_border + 4 * self.Y_step, self.Z]}

    def setRound(self, new_pos):
        for i in range(len(new_pos)):
            new_pos[i] = round(new_pos[i], 2)

        return new_pos

    def moveMarker(self, marker, dice_num):
        in_game = self.isMarkerInGame(marker)
        if in_game is True:
            self.setMarkerPos(marker, dice_num)
        else:
            if dice_num == 6:
                marker_color = re.split(r'_', marker)
                self.markers[marker] = self.marker_start[marker_color[0]]

        # self.setMarkerPos(marker, dice_num)
        return self.markers
    
    # Set new marker position. Need set move via stairs and wc input!!!
    def setMarkerPos(self, marker, dice_num):
        new_pos = []
        for i in list(self.marker_in_wc.keys()):
            if marker in self.marker_in_wc[i]:
                new_pos = self.setWCMarkerPos(self.markers[marker][0], self.markers[marker][1], dice_num, i)
                break

        if len(new_pos) == 0:
            new_pos = self.detectBorder(self.markers[marker][0], self.markers[marker][1], dice_num)

        new_pos = self.setRound(new_pos)
        new_pos = self.isPosInputWC(new_pos)
        self.markers[marker] = [new_pos[0], new_pos[1], self.markers[marker][2]]

    # Choose way to change position of marker
    def detectBorder(self, Xcoord, Ycoord, dice_num):
        new_pos = [Xcoord, Ycoord]
        #operator = self.getOperator(Xcoord, Ycoord)
        
        if Xcoord == self.bot_X_border:
            if Ycoord + dice_num * self.Y_step > self.left_Y_border:
                excess = math.fabs((Ycoord + dice_num * self.Y_step) - self.left_Y_border)
                lost_num = self.excessToDice(excess, self.Y_step)
                new_pos = [Xcoord + lost_num * self.X_step, self.left_Y_border]
            else:
                new_pos = [Xcoord, Ycoord + dice_num * self.Y_step]

        elif Xcoord == self.top_X_border:
            if Ycoord - dice_num * self.Y_step < self.right_Y_border:
                excess = math.fabs((Ycoord - dice_num * self.Y_step) - self.right_Y_border)
                lost_num = self.excessToDice(excess, self.Y_step)
                new_pos = [Xcoord - lost_num * self.X_step, self.right_Y_border]
            else:
                new_pos = [Xcoord, Ycoord - dice_num * self.Y_step]

        elif Ycoord == self.left_Y_border:
            if Xcoord + dice_num * self.X_step > self.top_X_border:
                excess = math.fabs((Xcoord + dice_num * self.X_step) - self.top_X_border)
                lost_num = self.excessToDice(excess, self.X_step)
                new_pos = [self.top_X_border, Ycoord - lost_num * self.Y_step]
            else:
                new_pos = [Xcoord + dice_num * self.X_step, Ycoord]

        elif Ycoord == self.right_Y_border:
            if Xcoord - dice_num * self.X_step < self.bot_X_border:
                excess = math.fabs((Xcoord - dice_num * self.X_step) - self.bot_X_border)
                lost_num = self.excessToDice(excess, self.X_step)
                new_pos = [self.bot_X_border, Ycoord + lost_num * self.Y_step]
            else:
                new_pos = [Xcoord - dice_num * self.X_step, Ycoord]

        return new_pos

    # It will replace detectBorder
    def detectBorderNew(self, Xcoord, Ycoord, dice_num):
        new_pos = [Xcoord, Ycoord]

        if Xcoord in [self.bot_X_border, self.top_X_border]:
            operator = self.getOperator(Xcoord, Ycoord)
            new_coord = self.countNewPos(Xcoord, dice_num, self.X_step, round(Xcoord, 2), operator[0])
            new_pos = [new_coord[0], Ycoord + operator[1] * self.Y_step]

        elif Ycoord in [self.left_Y_border, self.right_Y_border]:
            operator = self.getOperator(Xcoord, Ycoord)
            new_coord = self.countNewPos(Ycoord, dice_num, self.Y_step, round(Ycoord, 2), operator[1])
            new_pos = [Xcoord + operator[0] * self.X_step, new_coord[0]]

        return new_pos

    # Count excess to dice num
    def excessToDice(self, excess, step):
        dice_num = round(excess / step, 0)

        return dice_num

    # Need to replace detectBorder
    def countNewPos(self, coord, dice_num, step, border, operator):
        for i in [self.bot_X_border, self.top_X_border, self.left_Y_border, self.right_Y_border]:
            if coord == i:
                if coord + operator * dice_num * step > border:
                    excess = math.fabs((coord + operator * dice_num * step) - border)
                    lost_num = self.excessToDice(excess, step)
                    new_coord = [coord, lost_num]
                else:
                    new_coord = [coord + operator * dice_num * step, 0]

        return new_coord

    # Change marker position in WC
    def setWCMarkerPos(self, Xcoord, Ycoord, wc_key, dice_num):
        operator = self.getOperator(Xcoord, Ycoord)
        new_pos = [Xcoord, Ycoord]

        # If key in WC is 6 marker move under WC
        if wc_key == 6:
            for j in list(self.wc_coord[6].keys()):
                if Xcoord in self.wc_coord[6][j]:
                    if Ycoord in self.wc_coord[6][j]:
                        if j == 'top' or j == 'bot':
                            new_pos = [Xcoord - operator[0] * self.X_step, Ycoord]
                        elif j == 'left' or j == 'right':
                            new_pos = [Xcoord, Ycoord - operator[1] * self.Y_step]

        # If key in WC 1 or 3 marker move across WC
        else:
            for i in [1, 3]:
                if dice_num == i:
                    for j in list(self.wc_coord[i].keys()):
                        if Xcoord in self.wc_coord[i][j]:
                            if Ycoord in self.wc_coord[i][j]:
                                if j == 'top' or j == 'bot':
                                    new_pos = [Xcoord, Ycoord + operator[1] * self.Y_step]
                                    break
                                elif j == 'left' or j == 'right':
                                    new_pos = [Xcoord + operator[0] * self.X_step, Ycoord]
                                    break

        return new_pos

    # Get operator for changing coordinates of marker
    def getOperator(self, Xcoord, Ycoord):
        if Ycoord >= 0:
            Xoperator = 1
        elif Ycoord < 0:
            Xoperator = -1
        if Xcoord > 0:
            Yoperator = -1
        elif Xcoord < 0:
            Yoperator = 1

        return (Xoperator, Yoperator)

    # Get markers that in WC
    def getWCMarker(self):
        for i in list(self.markers.keys()):
            if self.marker[i] in self.wc_coord[1]['bot'] or self.marker[i] in self.wc_coord[1]['left'] or \
                    self.marker[i] in self.wc_coord[1]['top'] or self.marker[i] in self.wc_coord[1]['right']:
                self.marker_in_wc[1].append(i)
            elif self.marker[i] in self.wc_coord[3]['bot'] or self.marker[i] in self.wc_coord[3]['left'] or \
                    self.marker[i] in self.wc_coord[3]['top'] or self.marker[i] in self.wc_coord[3]['right']:
                self.marker_in_wc[3].append(i)
            elif self.marker[i] in self.wc_coord[6]['bot'] or self.marker[i] in self.wc_coord[6]['left'] or \
                    self.marker[i] in self.wc_coord[6]['top'] or self.marker[i] in self.wc_coord[6]['right']:
                self.marker_in_wc[6].append(i)

    def isWayFree(self, new_pos, dice_num, marker):
        points = self.createArrayOfPoints(new_pos, dice_num, marker)
        for i in list(self.all_markers.keys()):
            if round(self.all_markers[i][0], 2) in points[0] and round(self.all_markers[i][1], 2) in points[1]:
                return False

        for i in list(self.markers.keys()):
            if round(self.markers[i][0], 2) == new_pos[0] and round(self.markers[i][1], 2) == new_pos[1]:
                return False

    def createArrayOfPoints(self, new_pos, dice_num, marker):
        operator = self.getOperator(self.markers[marker][0], self.markers[marker][1])
        points = [[], []]
        if new_pos[0] - self.markers[marker][0] == 0:
            for j in range(1, dice_num):
                points[0].append(self.markers[marker][0] + operator[0] * j * self.X_step)

        elif new_pos[0] - self.markers[marker][0] != 0:
            lost_num = round((new_pos[0] - self.markers[marker][0]) / self.X_step, 0)
            for j in range(1, dice_num - lost_num + 1):
                points[0].append(self.markers[marker][0] + operator[0] * j * self.X_step)
            for j in range(1, lost_num):
                points[1].append(self.markers[marker][1] + operator[1] * j * self.Y_step)

        elif new_pos[1] - self.markers[marker][1] == 0:
            for j in range(1, dice_num):
                points[1].append(self.markers[marker][1] + operator[1] * j * self.Y_step)

        elif new_pos[1] - self.markers[marker][1] != 0:
            lost_num = round((new_pos[1] - self.markers[marker][1]) / self.Y_step, 0)
            for j in range(1, dice_num - lost_num + 1):
                points[1].append(self.markers[marker][1] + operator[1] * j * self.Y_step)
            for j in range(1, lost_num):
                points[0].append(self.markers[marker][0] + operator[0] * j * self.X_step)

        return points

    def isBitEnemyMarker(self, new_pos):
        for i in list(self.all_markers.keys()):
            if i not in list(self.markers.keys()):
                if round(self.all_markers[i][0], 2) == new_pos[0] and round(self.all_markers[i][1], 2) == new_pos[1]:
                    return True

    def isPosChange(self, new_pos, marker):
        pass

    def isPosInputWC(self, new_pos):
        operator = self.getOperator(new_pos[0], new_pos[1])
        print("inputWC")
        print(new_pos)
        print(self.wc_input)
        # for i in list(self.wc_input.keys()):
        #     print("inputWCfor")
        #     if new_pos[0] == self.wc_input[i][0] and new_pos[1] == self.wc_input[i][1]:
        #         print("inputWCif")
        #         if i == 'bot' or i == 'top':
        #             new_pos[0] = new_pos[0] + operator[0] * self.X_step
        #         elif i == 'left' or i == 'right':
        #             new_pos[1] = new_pos[1] + operator[1] * self.Y_step
        for i in list(self.wc_input.keys()):
            print("inputWCfor")
            if self.nearlyEqual(new_pos[0], self.wc_input[i][0]) is True and self.nearlyEqual(new_pos[1], self.wc_input[i][1]) is True:
                print("inputWCif")
                if i == 'bot' or i == 'top':
                    new_pos[0] = new_pos[0] + operator[0] * self.X_step
                elif i == 'left' or i == 'right':
                    new_pos[1] = new_pos[1] + operator[1] * self.Y_step

        return new_pos

    def isPosOnStairs(self, new_pos):
        for i in list(self.stairs.keys()):
            if new_pos[0] == self.stairs[i][0] and new_pos[1] == self.stairs[1]:
                if 'up' in i:
                    new_pos = self.posOnUpStairs(i)
                elif 'down' in i:
                    new_pos = self.posOnDownStairs(i)
        # for i in list(self.stairs.keys()):
        #     if self.nearlyEqual(new_pos[0], self.stairs[i][0]) is True and self.nearlyEqual(new_pos[1], self.stairs[i][1]) is True:
        #         if 'up' in i:
        #             new_pos = self.posOnUpStairs(i)
        #         elif 'down' in i:
        #             new_pos = self.posOnDownStairs(i)

        return new_pos

    def nearlyEqual(self, x, y):
        z = [1, -1]
        x = round(x, 1)
        y = round(y, 1)
        for i in z:
            delta_y = round(y + i * 0.1, 1)
            for j in z:
                delta_x = round(x + j * 0.1, 1)
                if delta_x == delta_y or x == delta_y or delta_x == y or x == y:
                    return True

    def posOnUpStairs(self, key):
        key_split = re.split(r'_', key)
        key = key_split[0] + '_' + key_split[1] + '_down'

        return self.stairs[key]

    def posOnDownStairs(self, key):
        key_split = re.split(r'_', key)
        key = key_split[0] + '_' + key_split[1] + '_up'

        return self.stairs[key]

    def isMarkerInGame(self, marker):
        for i in [self.top_X_border, self.bot_X_border, self.left_Y_border, self.right_Y_border]:
            if self.markers[marker][0] == i or self.markers[marker][1] == i:
                return True

# Detect 6 on dice for input in game new marker
def isSix(dices):
    for i in list(dices.values()):
        if i == 6:
            return True

# Choose more number on dices
def chooseDiceNum(dices):
    value_move = {'value_big': 0, 'value_small': 0, 'movement': 1}
    if dices['Dice_1'] > dices['Dice_2']:
        value_move['value_big'] = dices['Dice_1']
        value_move['value_small'] = dices['Dice_2']
    elif dices['Dice_2'] > dices['Dice_1']:
        value_move['value_big'] = dices['Dice_2']
        value_move['value_small'] = dices['Dice_1']
    elif dices['Dice_1'] == dices['Dice_2']:
        value_move['value_big'] = dices['Dice_1']
        value_move['value_small'] = dices['Dice_2']
        value_move['movement'] = 2

    return value_move
