# # Common imports
# import numpy as np
# import os

# # to make this notebook's output stable across runs
# def reset_graph(seed=42):
#     tf.reset_default_graph()
#     tf.set_random_seed(seed)
#     np.random.seed(seed)

# # To plot pretty figures
# import matplotlib
# import matplotlib.pyplot as plt
# plt.rcParams['axes.labelsize'] = 14
# plt.rcParams['xtick.labelsize'] = 12
# plt.rcParams['ytick.labelsize'] = 12


# def plot_image(image):
#     plt.imshow(image, cmap='gray', interpolation='nearest')
#     plt.axis('off')

# def plot_color_images(image):
#     plt.imshow(image.astype(np.uint8), interpolation='nearest')
#     plt.axis('off')

# import tensorflow as tf
# from sklearn.datasets import load_sample_image

# china = load_sample_image("china.jpg")
# flower = load_sample_image("flower.jpg")
# dataset = np.array([china, flower], dtype=np.float32)
# batch_size, height, width, channels = dataset.shape


# # Create 2 filters
# filters = np.zeros(shape=(7, 7, channels, 2), dtype=np.float32)
# filters[:, 3, :, 0] = 1  # vertical line
# filters[3, :, :, 1] = 1  # horizontal line

# X = tf.placeholder(tf.float32, shape=(None, height, width, channels))
# max_pool = tf.nn.max_pool(X, ksize=[1,2,2,1], strides=[1,2,2,1],padding="VALID")

# with tf.Session() as sess:
#     output = sess.run(max_pool, feed_dict={X: dataset})

# plt.imshow(output[0].astype(np.uint8))  # plot the output for the 1st image
# plt.show()


def comb(n, m):
    if m == 0:
        return 1
    res = 1
    for i in range(m):
        res *= n - i
    for i in range(m):
        res /= i + 1
    return res

# print(comb(7, 3))
n, m, h = map(int, input().strip().split())
h -= 1
s = list(map(int, input().strip().split()))

s_sum = sum(s)

if s_sum < n:
    print(-1)
else:
    if s[h] == 1:
        print(-1)
    elif s_sum == n:
        print(1)
    else:
        n1 = s[h] - 1
        n2 = s_sum - 1 - n1
        up = 0
        for i in range(1, min(n - 1, n1) + 1):
            up += comb(n1, i) * comb(n2, n - 1 - i)
        down = comb(n1 + n2, n - 1)
        print(up / down)