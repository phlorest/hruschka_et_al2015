from setuptools import setup


setup(
    name='cldfbench_hruschka_et_al2015',
    py_modules=['cldfbench_hruschka_et_al2015'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'hruschka_et_al2015=cldfbench_hruschka_et_al2015:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
