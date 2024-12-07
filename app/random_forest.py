import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import plotly.graph_objects as go

df = pd.read_csv('../individual_scripts/Park/users_details_dataset_cleaned.csv')
df['Birthday'] = pd.to_datetime(df['Birthday'])
df['Birthday_year'] = df['Birthday'].dt.year
current_year = datetime.now().year
df['age'] = current_year - df['Birthday_year']
df['completion_rate'] = df.apply(lambda row: 0 if row['Completed'] == 0 or row['Total Entries'] == 0 else row['Completed'] / row['Total Entries'], axis=1)
df = df[['age', 'Days Watched', 'Completed', 'Total Entries', 'completion_rate']]


def load_and_preprocess_data(df):
    features = ['age', 'Days Watched', 'Completed', 'Total Entries']
    target = 'completion_rate'
    
    X = df[features]
    y = df[target]

    X = X.fillna(X.mean())
    y = y.fillna(y.mean())
    
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.mean())
    
    for column in X.columns:
        percentile_99 = X[column].quantile(0.99)
        X[column] = X[column].clip(upper=percentile_99)
    
    y = y.clip(0, 1)
    
    return X, y

def train_and_predict(X, y):
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    return X_test, y_test, y_pred, rmse, r2, feature_importance, model, scaler

X, y = load_and_preprocess_data(df)
X_test, y_test, y_pred, rmse, r2, feature_importance, model, scaler = train_and_predict(X, y)


# --------------------------------------------------------------------------------
# Prediction

def predict_watching_stats(age, days_watched, model, scaler):
    avg_entries = 50
    avg_completed = 30
    features = np.array([[age, days_watched, avg_completed, avg_entries]])
    features_scaled = scaler.transform(features)
    predicted_rate = model.predict(features_scaled)[0]
    predicted_entries = int(days_watched)
    predicted_completed = int(predicted_entries * predicted_rate)
    
    return {
        'predicted_entries': predicted_entries,
        'predicted_completed': predicted_completed,
        'predicted_completion_rate': predicted_rate
    }

def predict_single_user(age, days_watched, model, scaler):
    """
    모델로부터 학습된 age별 rate를 사용하는 예측 함수
    """
    # mean values 계산
    mean_completed = X['Completed'].mean()
    mean_entries = X['Total Entries'].mean()
    
    # 모델을 사용하여 age별 rate 계산
    age_rates = {}
    age_groups = pd.cut(X['age'], bins=[0, 15, 25, 35, 45, 100])
    
    for age_group in age_groups.unique():
        group_data = X[age_groups == age_group]
        if len(group_data) > 0:
            
            group_input = np.array([[group_data['age'].mean(), 
                                   group_data['Days Watched'].mean(),
                                   mean_completed,
                                   mean_entries]])
            group_input_scaled = scaler.transform(group_input)
            age_rates[age_group] = model.predict(group_input_scaled)[0]
    
    current_age_group = pd.cut([age], bins=[0, 15, 25, 35, 45, 100])[0]
    base_rate = age_rates.get(current_age_group, 1.0)
    
    input_data = np.array([[age, days_watched, mean_completed, mean_entries]])
    input_scaled = scaler.transform(input_data)
    predicted_rate = model.predict(input_scaled)[0] * base_rate
    
    avg_entries_per_day = X['Total Entries'].sum() / X['Days Watched'].sum()
    predicted_entries = int(days_watched * avg_entries_per_day * base_rate)
    
    predicted_completed = int(predicted_entries * predicted_rate)
    
    predicted_entries = max(predicted_entries, 1)
    predicted_completed = max(min(predicted_completed, predicted_entries), 0)
    
    return predicted_completed, predicted_entries


input_age = st.number_input("Enter age:", value=0)
input_watched = st.number_input("Enter the total number of watching days:", value=0)

if int(input_age) > 0 and int(input_watched) > 0:
    
    completed, entries = predict_single_user(input_age, input_watched, model, scaler)
    st.write(f"The predicted total number of anime in user entry list: {entries}")
    st.write(f"The predicted number of anime completed by user: {completed}")
    

    # prediction = predict_watching_stats(input_age, input_watched, model, scaler)
    # st.write(f"The predicted total number of anime in user entry list: {prediction['predicted_entries']}")
    # st.write(f"The predicted number of anime completed by user: {prediction['predicted_completed']}")
    # st.write(f"The predicted completion Rate: {prediction['predicted_completion_rate']:.2f}")









# --------------------------------------------------------------------------------
# 3D visualization about residual
st.write("")
st.write("")
st.write("")
st.markdown('<p class="big-font">Application for showing 3D visualization about residual</p>', unsafe_allow_html=True)

def visualize_residual_analysis(y_test, y_pred):
    
    residuals = y_test - y_pred
    z = np.random.randn(len(y_pred))
   
    fig_3d = go.Figure(data=[go.Scatter3d(
       x=y_pred,
       y=np.abs(residuals),
       z=z,
       mode='markers',
       marker=dict(
           size=5,
           color=np.abs(residuals),
           colorscale='Viridis',
           opacity=0.6
       )
   )])
   
    fig_3d.update_layout(
       scene=dict(
           xaxis_title='Predicted Values',
           yaxis_title='Absolute Residuals',
           zaxis_title='Z Axis'
       ),
       width=600,
       height=600
   )
   
    st.plotly_chart(fig_3d)

visualize_residual_analysis(y_test, y_pred)

# --------------------------------------------------------------------------------
# Correlation Graph

def visualize_correlation_matrix(X_test, y_test, y_pred, correlation_columns, cmap_option='coolwarm'):
    corr_df = X_test.copy()
    corr_df['Actual'] = y_test
    corr_df['Predicted'] = y_pred
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df[correlation_columns].corr(), annot=True, cmap=cmap_option, center=0, fmt='.2f')
    plt.title('Correlation Matrix of Features and Predictions')
    plt.tight_layout()
    plt.show()

st.markdown("""
   <style>
   .big-font {
       font-size: 30px !important;
   }
   </style>
   """, unsafe_allow_html=True)
st.markdown('<p class="big-font">Application for showing correlation between features</p>', unsafe_allow_html=True)


col1, col2 = st.columns([1, 1])

with col1:
    options = {
        'age': st.checkbox('Age', value=True),
        'Days Watched': st.checkbox('The total number of watching days', value=True),
        'Completed': st.checkbox('The number of anime completed', value=True),
        'Total Entries': st.checkbox('The total number of anime in user entry list'),
        'Actual': st.checkbox('Actual value', value=True),
        'Predicted': st.checkbox('Predicted value'),
    }

    correlation_columns = [key for key, value in options.items() if value]

with col2:
    cmap_options = {
        'coolwarm': 'Red-White-Blue',
        'RdBu': 'Red to Blue',
        'viridis': 'Purple-Green-Yellow',
        'magma': 'Black-Purple-Yellow',
        'Blues': 'White to Blue',
        'Reds': 'White to Red',
        'YlOrRd': 'Yellow-Orange-Red',
        'RdYlBu': 'Red-Yellow-Blue',
        'BrBG': 'Brown-White-Blue-Green',
        'PiYG': 'Pink-Yellow-Green'
    }
    selected_cmap = st.selectbox('Select color map:', options=list(cmap_options.keys()), format_func=lambda x: cmap_options[x])

if len(correlation_columns) >= 2:
    visualize_correlation_matrix(X_test, y_test, y_pred, correlation_columns, selected_cmap)
    st.pyplot(plt)

# --------------------------------------------------------------------------------
# Distribution(Density) Graph

st.write("")
st.write("")
st.write("")
st.markdown('<p class="big-font">Application for showing distribution</p>', unsafe_allow_html=True)

def visualize_prediction_distribution(y_test, y_pred):
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data=y_test, label='Actual Values', color='blue', fill=True, alpha=0.3)
    sns.kdeplot(data=y_pred, label='Predicted Values', color='red', fill=True, alpha=0.3)
    plt.title('Distribution of Actual vs Predicted Values')
    plt.xlabel('Days Watched')
    plt.ylabel('Density')
    plt.legend()
    # plt.tight_layout()
    x_min, x_max = st.slider(
        'Select x-axis range',
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.1,
        label_visibility='collapsed',
    )
    plt.xlim(x_min, x_max)
    plt.show()

visualize_prediction_distribution(y_test, y_pred)
st.pyplot(plt)

# --------------------------------------------------------------------------------
# Scatter Graph

st.write("")
st.write("")
st.write("")
st.markdown('<p class="big-font">Application for showing scatters between features</p>', unsafe_allow_html=True)

col3, col4 = st.columns([1, 1])

scatter_features_options1 = {
    'Total Entries': 'The total number of anime in user entry list',
    'Completed': 'The number of anime completed',
    'age': 'Age',
    'Days Watched': 'The total number of watching days',
}

scatter_features_options2 = {
    'Completed': 'The number of anime completed',
    'age': 'Age',
    'Total Entries': 'The total number of anime in user entry list',
}

with col3:
    scatter_first_feature = st.selectbox('Select first feature:', options=list(scatter_features_options1.keys()), format_func=lambda x: scatter_features_options1[x])

with col4:
    scatter_second_feature = st.selectbox('Select second feature:', options=list(scatter_features_options2.keys()), format_func=lambda x: scatter_features_options2[x])

def visualize_feature_interactions(X_test, y_test, y_pred, feat1, feat2):
    errors = np.abs(y_test - y_pred)
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X_test[[feat1]], X_test[[feat2]], c=errors, cmap='YlOrRd', alpha=0.6)
    plt.colorbar(scatter, label='Prediction Error')
    plt.xlabel(feat1)
    plt.ylabel(feat2)
    plt.title(f'Feature Interaction: {feat1} vs {feat2}\nColor indicates prediction error')
    plt.tight_layout()
    plt.show()

visualize_feature_interactions(X_test, y_test, y_pred, scatter_first_feature, scatter_second_feature)
st.pyplot(plt)

# --------------------------------------------------------------------------------
# Boxplot depending on a feature

# st.write("")
# st.write("")
# st.write("")
# st.markdown('<p class="big-font">Application for showing error boxplots</p>', unsafe_allow_html=True)

# boxplot_features_options = {
#     'age': 'Age',
#     'Days Watched': 'The total number of watching days',
#     'Completed': 'The number of anime completed',
#     'Total Entries': 'The total number of anime in user entry list',
# }

# boxplot_first_feature = st.selectbox('Select feature:', options=list(boxplot_features_options.keys()), format_func=lambda x: boxplot_features_options[x])

# def visualize_error_boxplots(X_test, y_test, y_pred, feature):
#     errors = np.abs(y_test - y_pred)
#     results_df = pd.DataFrame(X_test.copy())
#     results_df['Error'] = errors
#     plt.figure(figsize=(15, 12))
#     plt.suptitle('Error Distribution by Feature Ranges', fontsize=16)
    
#     results_df[f'{feature}_bin'] = pd.qcut(results_df[feature], q=5, labels=[f'{i+1}' for i in range(5)])
    
#     sns.boxplot(data=results_df, x=f'{feature}_bin', y='Error')
#     plt.xlabel(f'{feature}', fontsize=24)
#     plt.ylabel('Error', fontsize=24)    
#     plt.tight_layout()
#     plt.show()

# visualize_error_boxplots(X_test, y_test, y_pred, boxplot_first_feature)
# st.pyplot(plt)


# --------------------------------------------------------------------------------
