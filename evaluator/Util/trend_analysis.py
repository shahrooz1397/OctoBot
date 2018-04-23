import numpy

from evaluator.Util.abstract_util import AbstractUtil
from config.cst import DIVERGENCE_USED_VALUE


class TrendAnalysis(AbstractUtil):

    # trend < 0 --> Down trend
    # trend > 0 --> Up trend
    @staticmethod
    def get_trend(data_frame, averages_to_use):
        trend = 0
        inc = round(1 / len(averages_to_use), 2)
        averages = []

        # Get averages
        for average_to_use in averages_to_use:
            averages.append(data_frame.tail(average_to_use).values.mean())

        for a in range(0, len(averages) - 1):
            if averages[a] - averages[a + 1] > 0:
                trend -= inc
            else:
                trend += inc

        return trend

    @staticmethod
    # TODO
    def detect_divergence(data_frame, indicator_data_frame):
        candle_data = data_frame.tail(DIVERGENCE_USED_VALUE)
        indicator_data = indicator_data_frame.tail(DIVERGENCE_USED_VALUE)

        total_delta = []

        for i in range(0, DIVERGENCE_USED_VALUE - 1):
            candle_delta = candle_data.values[i] - candle_data.values[i + 1]
            indicator_delta = indicator_data.values[i] - indicator_data.values[i + 1]
            total_delta.append(candle_delta - indicator_delta)

    @staticmethod
    def get_estimation_of_move_state_relatively_to_previous_moves_length(mean_crossing_indexes, pattern_move_size=1):

        # compute average move size
        time_averages = [(lambda a: mean_crossing_indexes[a+1]-mean_crossing_indexes[a])(a)
                         for a in range(len(mean_crossing_indexes)-1)]
        time_average = numpy.mean(time_averages)*pattern_move_size

        # higher than time_average => high chances to be at half of the move already
        if time_averages[-1] > time_average/2:
            return 1
        else:
            return time_averages[-1] / (time_average/2)

    @staticmethod
    def get_threshold_change_indexes(data_frame, threshold):

        # sub threshold values
        sub_threshold_indexes = data_frame.index[data_frame <= threshold]

        # remove consecutive sub-threshold values because they are not crosses
        threshold_crossing_indexes = []
        current_move_size = 1
        for i in range(len(sub_threshold_indexes)):
            index = sub_threshold_indexes[i]
            if not len(threshold_crossing_indexes):
                threshold_crossing_indexes.append(index)
            else:
                if threshold_crossing_indexes[-1] == index - current_move_size:
                    current_move_size += 1
                else:
                    threshold_crossing_indexes.append(sub_threshold_indexes[i-1])
                    threshold_crossing_indexes.append(index)
                    current_move_size = 1
        # add last index if data_frame ends above threshold and last threshold_crossing_indexes inferior
        # to data_frame size
        if sub_threshold_indexes[-1] < len(data_frame.index) and data_frame.iloc[-1] > threshold:
            threshold_crossing_indexes.append(sub_threshold_indexes[-1]+1)

        return threshold_crossing_indexes