#!/usr/bin/env python3

''''''''''''''''''''''''''''''''''''''''''''
' A script to generate a weekly timetable. '
'          Made by Florine de Geus         '
''''''''''''''''''''''''''''''''''''''''''''

import matplotlib.pyplot as plt
import argparse

DAYS = [
    'Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag',
    'Zondag'
]
COLORS = ['lightgreen', 'salmon', 'lightblue', 'violet', 'turquoise']
TYPE = ['Hoorcollege', 'Werkcollege', 'Tutoraat', 'Zelfstudie', 'Overig']
INPUT = 'schedule.dat'

if __name__ == '__main__':
    fig = plt.figure(figsize=(15, 7))
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='The schedule that has to be visualised')
    parser.add_argument('output', help='The name of the output file')
    args = parser.parse_args()

    with open(args.input) as f:
        lines = [l.strip() for l in f.readlines()]

        for line in lines:
            if line[0] == '#':
                continue

            data = line.split(maxsplit=5)
            subject = data[-1].replace(' ', '\n')
            data = list(map(float, data[:-1]))
            day = data[0] - 0.5
            start = data[1] + data[2] / 60
            end = start + data[3] / 60
            subj_type = int(data[4])

            plt.fill_between([day, day + 1], [start, start], [end, end],
                             color=COLORS[subj_type - 1],
                             edgecolor='k',
                             linewidth=0.5)
            plt.text(
                day + 0.5, (start + end) * 0.5,
                subject,
                ha='center',
                va='center',
                fontsize=11)

    ax = fig.add_subplot(111)
    ax.yaxis.grid()
    ax.set_xlim(0.5, len(DAYS) + 0.5)
    ax.set_ylim(23, 9)
    ax.set_yticks(range(9, 23, 2))
    ax.get_xaxis().set_visible(False)

    ax2 = ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(range(1, len(DAYS) + 1))
    ax2.set_xticklabels(DAYS)
    ax2.get_yaxis().set_visible(False)

    plt.savefig('{0}.png'.format(args.output.split('.')[0]), dpi=200)
