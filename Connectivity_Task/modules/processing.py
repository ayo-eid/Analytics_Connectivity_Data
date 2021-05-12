import pandas as pd


def clean_df(df):
    # 1. Drop variable "module_id" as 92.2% of it is missing, so no generalization analysis on it can be very useful
    df = df.drop(columns='module_id')
    # 2. drop nan values which are the last 22 rows of the dataset : the last 22 rows of event_time and event_type
    # variables are missing
    df = df.dropna()
    # 3. drop duplicates
    df = df.drop_duplicates()
    return df


def process(df):
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['event_day'] = df['event_time'].dt.date
    df['week_day'] = df['event_time'].dt.dayofweek
    week_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['week_day'] = df['week_day'].apply(lambda x: week_days[x])
    return df


def connectivity_ratio(df, attribute):
    df_graph = pd.DataFrame(df.groupby(attribute).event_type.value_counts())
    df_graph = df_graph.rename(columns={'event_type': 'count'})
    df_graph = df_graph.reset_index()
    return df_graph


def connectivity_ratio_ordered(df, attribute):
    df_graph = pd.DataFrame(df.groupby(attribute).event_type.value_counts())
    df_graph = df_graph.rename(columns={'event_type': 'count'})
    df_graph = df_graph.reset_index()
    df_graph = df_graph.sort_values(by='count', ascending=False)
    return df_graph
