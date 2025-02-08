
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS
# Target: src/ai/backend/kernel:dist

from setuptools import setup

setup(**{
    'author': 'Lablup Inc. and contributors',
    'classifiers': [
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    ],
    'description': 'Backend.AI Kernel Runner',
    'install_requires': (
        'aiohttp~=3.10.8',
        'attrs>=24.2',
        'boto3~=1.35',
        'janus~=1.0.0',
        'jupyter-client>=6.0',
        'msgpack~=1.1.0',
        'namedlist~=1.8',
        'pyzmq~=26.2',
        'types-six',
        'yarl~=1.13.1',
    ),
    'license': 'LGPLv3',
    'long_description': """# Backend.AI Kernel Runner
""",
    'long_description_content_type': 'text/markdown',
    'name': 'backend.ai-kernel',
    'namespace_packages': (
    ),
    'package_data': {
        'ai.backend.kernel': (
            'VERSION',
        ),
    },
    'packages': (
        'ai.backend.kernel',
        'ai.backend.kernel.app',
        'ai.backend.kernel.c',
        'ai.backend.kernel.cpp',
        'ai.backend.kernel.git',
        'ai.backend.kernel.golang',
        'ai.backend.kernel.haskell',
        'ai.backend.kernel.java',
        'ai.backend.kernel.julia',
        'ai.backend.kernel.lua',
        'ai.backend.kernel.nodejs',
        'ai.backend.kernel.octave',
        'ai.backend.kernel.php',
        'ai.backend.kernel.python',
        'ai.backend.kernel.python.drawing',
        'ai.backend.kernel.r',
        'ai.backend.kernel.r_server_ms',
        'ai.backend.kernel.rust',
        'ai.backend.kernel.scheme',
        'ai.backend.kernel.vendor',
        'ai.backend.kernel.vendor.aws_polly',
        'ai.backend.kernel.vendor.h2o',
    ),
    'project_urls': {
        'Documentation': 'https://docs.backend.ai/',
        'Source': 'https://github.com/lablup/backend.ai',
    },
    'python_requires': '>=3.12,<3.13',
    'url': 'https://github.com/lablup/backend.ai',
    'version': '25.2.0',
    'zip_safe': False,
})
