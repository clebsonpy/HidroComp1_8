import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
import colorlover as cl
import cufflinks as cf

from graphics.hydrogram_biuld import HydrogramBiuld


class HydrogramClean(HydrogramBiuld):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def plot(self):
        bandxaxis = go.XAxis(
            title="Data",
        )

        bandyaxis = go.YAxis(
            title="Vazão(m³/s)",
        )

        try:
            name = 'Hidrograma - %s' % self.data.name
            layout = dict(
                title=name.title(),
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                font=dict(family='Courier New, monospace', size=16, color='#7f7f7f'))

            data = [self._plot_one(self.data)]
            fig = dict(data=data, layout=layout)
            py.offline.plot(fig, filename='gráficos/'+ name.replace(' - ', '_') +'.html')
        except AttributeError:
            name = 'Hidrograma'
            layout = dict(
                title=name,
                xaxis=bandxaxis,
                yaxis=bandyaxis,
                font=dict(family='Courier New, monospace', size=16, color='#7f7f7f'))

            fig = dict(data=self._plot_multi(), layout=layout)
            py.offline.plot(fig, filename='gráficos/'+ name.replace(' - ', '_') +'.html')

    def _plot_multi(self):
        fig = []
        for i in self.data:
            fig.append(self.__plot_one(self.data[i]))

        return fig
