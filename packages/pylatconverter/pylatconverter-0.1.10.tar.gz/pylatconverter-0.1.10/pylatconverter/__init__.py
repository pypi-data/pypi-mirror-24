# -*- coding: utf-8 -*-
"""Top-level package for pyLatConverter."""

__author__ = """Francisco Salema"""
__email__ = 'x_salema@hotmail.com'
__version__ = '0.1.10'

import numpy as np

def to_matrix(M, equation=True, numbering=False, matrixStyle='b', toFile=None, writeStyle='w'):
    '''
    Function description

    Requirements:
        \\usepackage{amsmath}
    '''

    begin = ''
    mid = ''
    end = '\\end{' + str(matrixStyle) + 'matrix}\n'

    if equation:
        begin += '\\begin{equation'
        end += '\\end{equation'

        if numbering:
            begin += '}\n\t'
            end += '}\n'
        else:
            begin += '*}\n\t'
            end += '*}\n'
        
    begin += '\\begin{' + str(matrixStyle) + 'matrix}\n'

    mat = np.array(M)

    for line in mat:

        mid += '\t'
        if equation:
            mid += '\t'

        for i, element in enumerate(line):

            if i != len(line) - 1:
                mid += str(element) + ' & '
            else:
                mid += str(element) + ' \\\\\n'

    if equation:
        mid += '\t'

    matLatex = begin + mid + end

    if toFile:
        with open(toFile, writeStyle) as f:
            f.write(matLatex)

    print(matLatex)