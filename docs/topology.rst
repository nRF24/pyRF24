Network Topology
================

Network Levels
****************

Because of the hardware limitation's of the nRF24L01 transceiver, each network
is arranged in a levels where a parent can have up to 5 children. And each child can also have
up to 5 other children. This is not limitless because this network is designed for low-memory
devices. Consequently, all node's `Logical Address <logical_address>` are limited to 12-bit
integers and use an octal counting scheme.

- The master node (designated with the `Logical Address <logical_address>` ``0o0``)
  is always the only node in the lowest level (denoted as level 0).
- Child nodes are designated by the most significant octal digit in their
  `Logical Address <logical_address>`. A child node address' least significant digits are
  the inherited address of it's parent node. Nodes on level 1 only have 1 digit because they are
  children of the master node.

.. graphviz::

    graph network_hierarchy {
        bgcolor="#323232A1"
        newrank=true
        // ratio="0.65"
        node [
            fontcolor="#FEFEFE"
            fontsize=14
            fontname=Arial
        ]
        pad="0"
        margin="0"
        subgraph cluster_hierarchy {
            bgcolor="#24242400"
            color="#24242400"
            node [
                style=filled
                color="#FEFEFE7f"
            ]
            edge [color="#FEFEFE" style="setlinewidth(2)"]
            subgraph lvl_0 {
                "0o0" [
                    shape="circle"
                    style="radial"
                    fillcolor="0.85:#018268;0:#000"
                ]
            }
            subgraph lvl_1 {
                node [fillcolor="#3E0180"]
                "0o1" "0o2" "0o3" "0o4" "0o5"
            }
            subgraph lvl_2 {
                node [fillcolor="#014B80"]
                "0o14" "0o24" "0o34" "0o44" "0o54"
            }
            subgraph lvl_3 {
                node [fillcolor="#0E6902"]
                "0o124" "0o224" "0o324" "0o424" "0o524"
            }
            subgraph lvl_4 {
                node [fillcolor="#80010B"]
                "0o1324" "0o2324" "0o3324" "0o4324" "0o5324"
            }
            "0o0" -- "0o4" -- "0o24" -- "0o324" -- "0o1324"
            "0o0" -- "0o1"; "0o0" -- "0o2"; "0o0" -- "0o3"; "0o0" -- "0o5"
            "0o4" -- "0o14"; "0o4" -- "0o34"; "0o4" -- "0o44"; "0o4" -- "0o54"
            "0o24" -- "0o124"; "0o24" -- "0o224"; "0o24" -- "0o424"; "0o24" -- "0o524"
            "0o324" -- "0o2324"; "0o324" -- "0o3324"; "0o324" -- "0o4324"; "0o324" -- "0o5324"
        }
        subgraph cluster_legend {
            bgcolor="#242424"
            color="#24242400"
            "Legend" [
                color="#FEF9A9"
                shape=plain
                margin=0
                label=<
                        <TABLE CELLBORDER="0" CELLSPACING="8">
                            <TR>
                                <TD BORDER="1" SIDES="B" COLSPAN="3">Legend</TD>
                            </TR>
                            <TR>
                                <TD>Network Level 0</TD>
                                <TD BORDER="1" STYLE="rounded,radial" BGCOLOR="#000:#018268">        </TD>
                            </TR>
                            <TR>
                                <TD>Network Level 1</TD>
                                <TD BORDER="1" STYLE="rounded" BGCOLOR="#3E0180">        </TD>
                            </TR>
                            <TR>
                                <TD>Network Level 2</TD>
                                <TD BORDER="1" STYLE="rounded" BGCOLOR="#014B80">        </TD>
                            </TR>
                            <TR>
                                <TD>Network Level 3</TD>
                                <TD BORDER="1" STYLE="rounded" BGCOLOR="#0E6902">        </TD>
                            </TR>
                            <TR>
                                <TD>Network Level 4</TD>
                                <TD BORDER="1" STYLE="rounded" BGCOLOR="#80010B">        </TD>
                            </TR>
                            <TR>
                                <TD BORDER="1" SIDES="T" COLSPAN="3">Nodes are labeled<BR/>in octal numbers</TD>
                            </TR>
                        </TABLE>
                >
            ]
        }
    }

Hopefully, you should see the pattern. There can be up to a maximum of 5 network levels (that's
0-4 ordered from lowest to highest).

For a message to travel from node ``0o124`` to node ``0o3``, it must be passed through any applicable
network levels. So, the message flows ``0o124`` -> ``0o24`` -> ``0o4`` -> ``0o0`` -> ``0o3``.

A single network can potentially have a maximum of 781 nodes (all operating on the same
:attr:`~pyrf24.rf24.RF24.channel`), but for readability reasons, the following
graph only demonstrates

- the master node (level 0) and it's 5 children (level 1)
- level 2 only shows the 1\ :sup:`st` and 2\ :sup:`nd` children of parents on level 1
- level 3 only shows the 3\ :sup:`rd` and 4\ :sup:`th` children of parents on level 2
- level 4 only shows the 5\ :sup:`th` children of parents on level 3


.. graphviz::

    graph network_levels {
        layout=twopi
        bgcolor="#323232A1"
        ratio="0.825"
        node [
            style=filled
            fontcolor="#FEFEFE"
            color="#FEFEFE7f"
            fontsize=14
            fontname=Arial
        ]
        edge [color="#FEFEFE" style="setlinewidth(2)"]
        ranksep="0.85:0.9:0.95:1.1"
        subgraph lvl_0 {
            "0o0" [
                root=true
                shape="circle"
                style="radial"
                fillcolor="0.9:#018268;0:#000"
            ]
        }
        subgraph lvl_1 {
            node [fillcolor="#3E0180"]
            "0o1" "0o2" "0o3" "0o4" "0o5"
        }
        subgraph lvl_2 {
            node [fillcolor="#014B80"]
            "0o11" "0o21" "0o12" "0o22" "0o13" "0o23" "0o14" "0o24" "0o15" "0o25"
        }
        subgraph lvl_3 {
            node [fillcolor="#0E6902"]
            "0o311" "0o411" "0o321" "0o421" "0o312" "0o412" "0o322" "0o422" "0o313" "0o413"
            "0o323" "0o423" "0o314" "0o414" "0o324" "0o424" "0o315" "0o415" "0o325" "0o425"
        }
        subgraph lvl_4 {
            node [fillcolor="#80010B"]
            "0o5311" "0o5411" "0o5321" "0o5312" "0o5421" "0o5313" "0o5314" "0o5315" "0o5322"
            "0o5323" "0o5324" "0o5325" "0o5412" "0o5423" "0o5422" "0o5413" "0o5414" "0o5424"
            "0o5415" "0o5425"
        }
        "0o0" -- "0o1" -- "0o11" -- "0o311" -- "0o5311"
        "0o0" -- "0o2" -- "0o12" -- "0o312" -- "0o5312"
        "0o0" -- "0o3" -- "0o13" -- "0o313" -- "0o5313"
        "0o0" -- "0o4" -- "0o14" -- "0o314" -- "0o5314"
        "0o0" -- "0o5" -- "0o15" -- "0o315" -- "0o5315"
        "0o1" -- "0o21" -- "0o321" -- "0o5321"
        "0o2" -- "0o22" -- "0o322" -- "0o5322"
        "0o3" -- "0o23" -- "0o323" -- "0o5323"
        "0o4" -- "0o24" -- "0o324" -- "0o5324"
        "0o5" -- "0o25" -- "0o325" -- "0o5325"
        "0o11" -- "0o411" -- "0o5411"
        "0o21" -- "0o421" -- "0o5421"
        "0o12" -- "0o412" -- "0o5412"
        "0o22" -- "0o422" -- "0o5422"
        "0o13" -- "0o413" -- "0o5413"
        "0o23" -- "0o423" -- "0o5423"
        "0o14" -- "0o414" -- "0o5414"
        "0o24" -- "0o424" -- "0o5424"
        "0o15" -- "0o415" -- "0o5415"
        "0o25" -- "0o425" -- "0o5425"
    }

.. _physical_address:
.. _logical_address:

Physical addresses vs Logical addresses
***************************************

- The Physical address is the 5-byte address assigned to the radio's data pipes.
- The Logical address is the 12-bit integer representing a network node.
  The Logical address uses an octal counting scheme. A valid Logical Address must only
  contain octal digits in range [1, 5]. The master node is the exception for it uses the
  number ``0``

  .. tip::
      Use the :py:meth:`~pyrf24.rf24_network.RF24Network.is_address_valid()`
      function to programmatically check a Logical Address for validity.

.. note::
    Remember that the nRF24L01 only has 6 data pipes for which to receive or transmit.
    Since only data pipe 0 can be used to transmit, the other other data pipes 1-5 are
    devoted to receiving transmissions from other network nodes; data pipe 0 also receives
    multicasted messages about the node's network level).

Translating Logical to Physical
-------------------------------

Before translating the Logical address, a single byte is used repetitively as the
base case for all bytes of any Physical Address. This byte is the address prefix
(stored internally and unexposed) in the `RF24Network` class. By default the
address prefix has a single byte value of ``0xCC``.

The `RF24Network` class also has a predefined internal (unexposed) array of bytes used for translating
unique Logical addresses into unique Physical addresses. This list is called
address suffix. By default the address suffix has 6-byte value of
``{ 0xC3, 0x3C, 0x33, 0xCE, 0x3E, 0xE3 }`` where the order of bytes pertains to the
data pipe number and child node's most significant byte in its Physical Address.

For example:
    The Logical Address of the network's master node is ``0``. The radio's pipes
    1-5 start with the address prefix. To make each pipe's Physical address unique
    to a child node's Physical address, the address suffix is used.

    The Logical address of the master node: ``0o0``

    .. csv-table::
        :header: "pipe", "Physical Address (hexadecimal)"

        1, ``CC CC CC CC 3C``
        2, ``CC CC CC CC 33``
        3, ``CC CC CC CC CE``
        4, ``CC CC CC CC 3E``
        5, ``CC CC CC CC E3``

    The Logical address of the master node's first child: ``0o1``

    .. csv-table::
        :header: "pipe", "Physical Address (hexadecimal)"

        1, ``CC CC CC 3C 3C``
        2, ``CC CC CC 3C 33``
        3, ``CC CC CC 3C CE``
        4, ``CC CC CC 3C 3E``
        5, ``CC CC CC 3C E3``

    The Logical address of the master node's second child: ``0o2``

    .. csv-table::
        :header: "pipe", "Physical Address (hexadecimal)"

        1, ``CC CC CC 33 3C``
        2, ``CC CC CC 33 33``
        3, ``CC CC CC 33 CE``
        4, ``CC CC CC 33 3E``
        5, ``CC CC CC 33 E3``

    The Logical address of the master node's third child's second child's first child: ``0o123``

    .. csv-table::
        :header: "pipe", "Physical Address (hexadecimal)"

        1, ``CC 3C 33 CE 3C``
        2, ``CC 3C 33 CE 33``
        3, ``CC 3C 33 CE CE``
        4, ``CC 3C 33 CE 3E``
        5, ``CC 3C 33 CE E3``


RF24Mesh connecting process
***************************

As noted above, a single network *can* have up to 781 nodes. This number also includes
up to 255 RF24Mesh nodes. The key difference from the user's perspective is that RF24Mesh
API does not publicly use a `Logical Address <logical_address>`. Instead the RF24Mesh API
relies on a :attr:`~pyrf24.rf24_mesh.RF24Mesh.node_id` number to identify a RF24Mesh node
that may use a different  `Logical Address <logical_address>` (which can change based on
the node's physical location).

.. important::
    Any network that will use RF24mesh for a child node needs to have a RF24Mesh
    master node. This will not interfere with RF24Network nodes since the RF24Mesh API
    is layered on top of the RF24Network API.

To better explain the difference between a node's `mesh_address` vs a node's
:attr:`~pyrf24.rf24_mesh.RF24Mesh.node_id`, we will examine the connecting process for a
RF24Mesh node. These are the steps performed when calling `renew_address()`:

1. Any RF24Mesh node not connected to a network will use the `Logical Address <logical_address>`
   ``0o444`` (that's ``2340`` in decimal). It is up to the network administrator to ensure that
   each RF24Mesh node has a unique :attr:`~pyrf24.rf24_mesh.RF24Mesh.node_id` (which is limited
   to the range [0, 255]).

   .. hint::
       Remember that ``0`` is reserved the master node's
       :attr:`~pyrf24.rf24_mesh.RF24Mesh.node_id`.
2. To get assigned a `Logical Address <logical_address>`, an unconnected node must poll the
   network for a response (using a `NETWORK_POLL` message). Initially this happens on the
   network level 0, but consecutive attempts will poll higher network levels (in order of low to
   high) if this process fails.
3. When a polling transmission is responded, the connecting mesh node sends an address
   request which gets forwarded to the master node when necessary (using a
   `NETWORK_REQ_ADDRESS` message).
4. The master node will process the address request and respond with a `mesh_address`
   (using a `NETWORK_ADDR_RESPONSE` message). If there is no available occupancy on the
   network level from which the address request originated, then the master node will
   respond with an invalid `Logical Address <logical_address>`.
5. Once the requesting node receives the address response (and the assigned address is
   valid), it assumes that as the `mesh_address` while maintaining its
   :attr:`~pyrf24.rf24_mesh.RF24Mesh.node_id`.

   - The connecting node will verify its new address by calling `check_connection()`.
   - If the assigned address is invalid or `check_connection()` returns `False`, then
     the connecting node will re-start the process (step 1) on a different network level.

Points of failure
-----------------

This process happens over a span of a few milliseconds. However,

- If the connecting node is physically moving throughout the network very quickly,
  then this process will take longer and is likely to fail.
- If a master node is able to respond faster than the connecting node can prepare itself
  to receive, then the process will fail entirely. This failure about faster master
  nodes often results in some slower RF24Mesh nodes only being able to connect to the
  network through another non-master node.

If you run into trouble with this connection process, then please
`open an issue on github <https://github.com/nRF24/pyRF24/issues>`_
and describe the situation with as much detail as possible.
