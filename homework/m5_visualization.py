"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    # TODO: 你的程式碼
    df = _load_data()
    order = df['category'].value_counts().index

    fig = plt.figure(figsize=(8, 4))
    sns.countplot(                 
    data=df,
    x='category',
    order=order,                
    palette='viridis',
    hue='category',
    legend=False,               
)
    plt.title('Orders by Category')
    plt.xlabel('Category')
    plt.ylabel('Order Count')
    plt.tight_layout()
    return fig         


def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig = plt.figure(figsize=(8,4))
    sns.histplot(data= df, x= 'amount',bins=20)
    plt.title('Distribution of Order Amount')
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    plt.tight_layout()
    return fig


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig = plt.figure(figsize=(8,4))
    region_rev = df.groupby('region')['amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=region_rev,x='region',y='amount',palette='viridis',hue='region',legend=True)
    plt.title('Revenue by Region')
    plt.xlabel('Region')
    plt.ylabel('amount')
    plt.tight_layout()
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    # TODO: 你的程式碼
    df = _load_data()
    df_ns = df[df['region'].isin(['North','South'])].copy()
    df_ns['month'] = df_ns['order_date'].dt.to_period('M').dt.to_timestamp()
    monthly = df_ns.groupby(['month','region'])['amount'].sum().reset_index()

    fig = plt.figure(figsize=(8,4))
    sns.lineplot(data = monthly, x='month',y='amount',hue='region',marker='o')
    plt.title('Monthly Revenue Trend: North vs South')
    plt.xlabel('Month')
    plt.ylabel('Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig = plt.figure(figsize=(8,4))
    sns.boxplot(data=df,x= 'vip_level',y= 'amount',order=['Bronze','Silver','Gold','Platinum'],palette='viridis',hue='vip_level',legend=False)
    plt.title('Order Amount Distribution by VIP Level')
    plt.xlabel('VIP Level')
    plt.ylabel('Amount')
    plt.tight_layout()
    return fig


def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    # TODO: 你的程式碼
    df = _load_data()
    fig = plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='unit_price', y='amount',hue='category',alpha = 0.5)
    plt.title('Unit Price vs Order Amount')
    plt.xlabel('Unit Price')
    plt.ylabel('Amount')
    plt.tight_layout()
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    """
    針對指定類別，畫 2×2 的 subplot dashboard：
    1. 左上：該類別月營收趨勢 (折線圖)
    2. 右上：該類別各地區營收 (長條圖)
    3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    4. 右下：該類別訂單金額分佈 (直方圖)

    回傳 matplotlib Figure 物件
    提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    """
    # TODO: 你的程式碼
    df = _load_data()
    df_cat = df[df['category'] == category].copy()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    df_cat['month'] = df_cat['order_date'].dt.to_period('M').dt.to_timestamp()
    monthly = df_cat.groupby('month')['amount'].sum().reset_index()
    sns.lineplot(data=monthly, x='month', y='amount', marker='o', ax=axes[0, 0])
    axes[0, 0].set_title(f'{category} Monthly Revenue Trend')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Revenue')
    axes[0, 0].tick_params(axis='x', rotation=45)

    region_rev = df_cat.groupby('region')['amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=region_rev,x='region',y='amount',palette='viridis',hue='region',legend=False,ax=axes[0,1])
    axes[0, 1].set_title(f'{category} Revenue by Region')
    axes[0, 1].set_xlabel('Region')
    axes[0, 1].set_ylabel('Revenue')

    top5 = df_cat.groupby('product_name')['amount'].sum().nlargest(5).reset_index()
    sns.barplot(data=top5,x='amount',y= 'product_name',palette='coolwarm',hue='product_name',legend=False,ax=axes[1,0])
    axes[1, 0].set_title(f'{category} Top 5 Products')
    axes[1, 0].set_xlabel('Revenue')
    axes[1, 0].invert_yaxis()

    sns.histplot(data=df_cat, x='amount', bins=20, kde=True, ax=axes[1, 1])
    axes[1, 1].set_title(f'{category} Order Amount Distribution')
    axes[1, 1].set_xlabel('Amount')
    axes[1, 1].set_ylabel('Frequency')

    fig.suptitle(f'Dashboard: {category}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig
