import matplotlib.pyplot as plt

def visualize_contributions(contribution_data):
    labels = contribution_data.keys()
    sizes = contribution_data.values()
    total = sum(sizes)

    sizes = [s / total * 100 for s in sizes]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Contributions by Contributor')
    plt.show()