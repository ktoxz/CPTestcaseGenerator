{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "def symmetry(n):\n",
    "    a=0\n",
    "    if n[0,0]==n[2,2]:\n",
    "        if n[0,1]==n[2,1]:\n",
    "            if n[0,2]==n[2,0]:\n",
    "                if n[1,0]==n[1,2]:\n",
    "                    a=1\n",
    "    if a==0:\n",
    "        return 'NO'\n",
    "    else:\n",
    "        return 'YES'"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}