import matplotlib.pyplot as plt
import numpy as np
import csv


if __name__ == '__main__':
    with open('hand_landmarks.csv') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        all_landmarks = dict()
        num_frames = 0
        for row in reader:
            num_frames += 1
            num = 1
            for i in range(((len(row) - 1) // 3)):  # количество "троек" координат
                k = i * 3 + 1  # номер в row

                landmark = (row[k], row[k + 1], row[k + 2])  # тройка координат (x, y, z)
                if num not in all_landmarks.keys():
                    all_landmarks[num] = [landmark]
                else:
                    all_landmarks[num].append(landmark)
                num += 1
        all_good_landmarks = dict()
        for num in all_landmarks:
            landmarks = all_landmarks[num]
            xs, ys, zs = list(), list(), list()
            for landmark in landmarks:
                xs.append(float(landmark[0]))
                ys.append(float(landmark[1]))
                zs.append(float(landmark[2]))
            xs, ys, zs = tuple(xs), tuple(ys), tuple(zs)
            all_good_landmarks[num] = {'x': xs, 'y': ys, 'z': zs}
            # print(f'{num} = {all_landmarks[num]}')
        for num in all_good_landmarks:
            print(all_good_landmarks[num])
        all_landmarks = all_good_landmarks
        print(all_landmarks[1]['x'])
        fig = plt.figure(figsize=(10, 20))

        for i in range(7):
            for j in range(3):
                plt.subplot2grid((7, 3), (i, j))
        for num, ax in enumerate(fig.axes):
            if num < 21:
                ax.plot(range(1, num_frames + 1), all_landmarks[num + 1]['x'], label='x')
                ax.plot(range(1, num_frames + 1), all_landmarks[num + 1]['y'], label='y')
                ax.plot(range(1, num_frames + 1), all_landmarks[num + 1]['z'], label='z')
                ax.text(0.5, 0.5, str(num+1), color='b')
                # ax.legend()
                ax.grid(True)
        plt.show()
        # plt.plot(range(1, num_frames + 1), all_landmarks[1]['x'], label='x')
        # plt.plot(range(1, num_frames + 1), all_landmarks[1]['y'], label='y')
        # plt.plot(range(1, num_frames + 1), all_landmarks[1]['z'], label='z')
        # plt.grid(True)
        # plt.legend()
        # plt.show()
        # fig = plt.figure(2)
        # plt.plot(range(10), [0.111, 0.222, 0.333, 0.555, 0.444, 0.777, 0.888, 0.666, 0.999, 0.000])
        # plt.show()

