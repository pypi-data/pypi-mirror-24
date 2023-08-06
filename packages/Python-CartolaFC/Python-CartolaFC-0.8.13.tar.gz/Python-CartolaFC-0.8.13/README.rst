Python Cartola FC API
=====================

|PyPi Version| |Downloads| |Build Status| |Coverage Status|
|Requirements Status| |Development Status| |License|

Uma interface em Python para a API Rest do Cartola FC.

Índice
======

-  `Sobre este projeto <#sobre-este-projeto>`__
-  `Versões <#versoes>`__
-  `Instalação <#instalacao>`__
-  `Exemplo <#exemplo>`__
-  `Contribuintes <#contribuintes>`__
-  `Direitos autorais e licença <#direitos-autorais-e-licenca>`__

Sobre este projeto
------------------

Este projeto é uma interface em Python para a API REST do Cartola FC.
`Cartola FC <https://cartolafc.globo.com/>`__ é um esporte fantasy sobre
futebol, ou seja, é um jogo fictício no qual as pessoas montam seus
times com jogadores de futebol da vida real. Foi lançado no ano de 2005.

Criado e mantido por `Globo.com <http://www.globo.com/>`__ e promovido
pelo canal de TV por assinatura `Sportv <http://sportv.globo.com/>`__,
este jogo de futebol virtual conta com mais de 3 milhões de usuários
registrados. Logo na abertura da temporada 2016, o jogo registrou a sua
melhor marca entre times escalados em uma única rodada em 12 anos de
história do fantasy, incríveis 2.723.915 de usuários montaram as suas
equipes para a primeira rodada do Campeonato Brasileiro de 2016.

Felizmente, os designers forneceram uma excelente e completa interface
REST. Essa biblioteca inclui essa interface como objetos de python mais
convencionais.

Versões
-------

Este projeto foi testado e funciona em Python 2.7, 3.3, 3.4, 3.5 e 3.6.

Instalação
----------

PyPI:

.. code:: bash

        $ pip install Python-CartolaFC

Ou baixando o código fonte e executando:

.. code:: bash

        $ python setup.py install

Versão em desenvolvimento:

.. code:: bash

        $ pip install git+https://github.com/vicenteneto/python-cartolafc.git#egg=Python-CartolaFC

Exemplo
-------

A API Python-CartolaFC destina-se a mapear os objetos no CartolaFC (por
exemplo, Atleta, Clube, Liga, Equipe) em objetos Python facilmente
gerenciados:

.. code:: python

    >>> import cartolafc
    >>> api = cartolafc.Api()
    >>> time = api.time(nome='Falydos FC')
    >>> time.ultima_pontuacao
    48.889892578125
    >>> time.info.nome
    u'Falydos FC'

Mais exemplos disponíveis no Github:
https://github.com/vicenteneto/python-cartolafc/tree/master/examples

Contribuintes
-------------

Identificou algum bug ou tem alguma requisição de funcionalidade nova?
`Por favor, abra uma nova
issue <https://github.com/vicenteneto/python-cartolafc/issues/new%3E>`__.

**Vicente Neto (criador)** - https://github.com/vicenteneto\ 

Direitos autorais e licença
---------------------------

Copyright 2017-, Vicente Neto. Este projeto é licenciado sob a `Licença
MIT <https://github.com/vicenteneto/python-cartolafc/blob/master/LICENSE>`__.

.. |PyPi Version| image:: https://img.shields.io/pypi/v/python-cartolafc.svg
   :target: https://pypi.python.org/pypi/python-cartolafc
.. |Downloads| image:: https://img.shields.io/pypi/dm/python-cartolafc.svg
   :target: https://pypi.python.org/pypi/python-cartolafc
.. |Build Status| image:: https://travis-ci.org/vicenteneto/python-cartolafc.svg?branch=master
   :target: https://travis-ci.org/vicenteneto/python-cartolafc
.. |Coverage Status| image:: https://coveralls.io/repos/github/vicenteneto/python-cartolafc/badge.svg?branch=master
   :target: https://coveralls.io/github/vicenteneto/python-cartolafc?branch=master
.. |Requirements Status| image:: https://requires.io/github/vicenteneto/python-cartolafc/requirements.svg?branch=master
   :target: https://requires.io/github/vicenteneto/python-cartolafc/requirements/?branch=master
.. |Development Status| image:: http://img.shields.io/:status-production/stable-brightgreen.svg
   :target: https://github.com/vicenteneto/python-cartolafc
.. |License| image:: http://img.shields.io/:license-mit-blue.svg
   :target: https://github.com/vicenteneto/python-cartolafc/blob/master/LICENSE
