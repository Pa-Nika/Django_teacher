import matplotlib.pyplot as plt
import pandas as pd


class Graph:
    def __init__(self, df_video):
        self.df_video = df_video

    def plot_and_save_graph(self):

        # Преобразование столбца 'duration' в timedelta
        # self.df_video['duration'] = pd.to_timedelta(self.df_video['duration'])
        self.df_video = self.df_video.sort_values(by='duration')

        plt.figure(figsize=(10, 6))
        plt.plot(self.df_video['duration'], self.df_video['mark'], marker='o')
        plt.xlabel('Длительность видео')
        plt.ylabel('Оценка')
        plt.title('График оценок в зависимости от длительности видео')
        plt.grid(True)

        plt.savefig('graph.png')
