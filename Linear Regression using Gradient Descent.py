import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

"""def train(x,y):
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(x,y)
    return model"""

def avg_loss(spendings,sales,w,b):
    N=len(spendings)
    total_error=0.0
    for i in range(N):
        total_error+=(sales[i]-w*spendings[i]*b)**2
    return total_error/float(N)

def update_w_and_b(spendings, sales, w, b, alpha):
    dl_dw=0.0
    dl_db=0.0
    N=len(spendings)

    for i in range(N):
        dl_dw+=-2*spendings[i]*(sales[i]-(w*spendings[i]+b))
        dl_db+=-2*(sales[i]-(w*spendings[i]+b))

    w=w-(1/float(N))*dl_dw*alpha
    b=b-(1/float(N))*dl_db*alpha
    
    return w,b

def visualize(spendings, sales, w, b, epoch):
    clear_output(wait=True) 
    plt.figure(figsize=(10, 6))
    
    plt.scatter(spendings, sales, color="blue", label="Data Points")
    
    x_vals = np.linspace(min(spendings), max(spendings), 100)
    y_vals = w * x_vals + b
    plt.plot(x_vals, y_vals, color="red", label=f"Regression Line (Epoch {epoch})")
    
    plt.title("Evolution of Regression Line")
    plt.xlabel("Spendings")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)
    plt.show()


def train(spendings, sales, w, b, alpha, epochs):
    for e in range(epochs):
        w,b=update_w_and_b(spendings, sales,w,b,alpha)
        if e%400==0:
            visualize(spendings, sales, w, b, e)
    return w,b

def predict(x,w,b):
    return w*x+b

excel_file = "Grad dec data.xlsx"
df = pd.read_excel(excel_file)
spendings = df.iloc[:, 0].to_numpy() 
sales = df.iloc[:, 1].to_numpy() 

w,b=train(spendings, sales, 0.0,0.0,0.001,2000)
y_new=predict(23.0,w,b)
"""model=train(spendings,sales)
y_new=model.predict(23.0)"""

print(y_new)

