from pyspark.sql.session import SparkSession
from pyspark.sql.functions import col, abs


class OutlierDetector:
    """
    Outlier detection for pyspark dataframes.
    """
    def __init__(self, df, column):
        self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()
        self._df = df
        self._column = column

        self.medianValue = median(self._df, self._column)

        absolute_deviation = (self._df
                             .select(self._column)
                             .orderBy(self._column)
                             .withColumn(self._column, abs(col(self._column) - self.medianValue))
                             .cache())

        self.madValue = median(absolute_deviation, column)

        self.threshold = 2

        self._limits = []
        self._limits.append(round((self.medianValue - self.threshold * self.madValue), 2))
        self._limits.append(round((self.medianValue + self.threshold * self.madValue), 2))

    def run(self):
        """
        Get list of values within accepted range, without duplicates
        """

        limits = self._limits
        column = self._column

        values_within_range = list(set((self._df
                                      .rdd.map(lambda x: x[column])
                                      .filter(lambda x: x >= limits[0] and x <= limits[1])
                                      .collect())))

        return values_within_range

    def outliers(self):
        """
        Get list of values within accepted range, without duplicates
        """

        limits = self._limits
        column = self._column

        values_without_range = list(set((self._df
                                       .rdd.map(lambda x: x[column])
                                       .filter(lambda x: x < limits[0] or x > limits[1])
                                       .collect())))

        return values_without_range

    def delete_outliers(self):
        """
        Deletes all rows where values in the column are outliers
        """

        limits = self._limits
        column = self._column

        func = lambda x: (x >= limits[0]) & (x <= limits[1])
        self._df = self._df.filter(func(col(column)))

        return self._df

    def get_data_frame(self):
        """
        :rtype: pyspark.sql.dataframe.DataFrame
        """
        self.get_data_frame()


def median(df, column):
    return df.approxQuantile(column, [0.5], 0.01)[0]
