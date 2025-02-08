from typing                                               import Type, Set, Any, Dict
from osbot_utils.utils.Dev                                import pprint
from mgraph_db.mgraph.domain.Domain__MGraph__Graph        import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node        import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge        import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Index__Data import Schema__MGraph__Index__Data
from osbot_utils.helpers.Obj_Id                           import Obj_Id
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.utils.Json                               import json_file_create, json_load_file

class MGraph__Index(Type_Safe):
    index_data : Schema__MGraph__Index__Data

    # todo: refactor all these add_* methods to an MGraph__Index__Create class (which will hold all the login to create the index)
    #       the main methods in this class should be focused on easy access to the MGraph index data
    def add_node(self, node: Schema__MGraph__Node) -> None:                         # Add a node to the index
        node_id   = node.node_id
        node_type = node.node_type.__name__

        if node_id not in self.index_data.nodes_to_outgoing_edges:                  # Initialize sets if needed
            self.index_data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.index_data.nodes_to_incoming_edges:
            self.index_data.nodes_to_incoming_edges[node_id] = set()


        if node_type not in self.index_data.nodes_by_type:                          # Add to type index
            self.index_data.nodes_by_type[node_type] = set()
        self.index_data.nodes_by_type[node_type].add(node_id)

        self.index_node_data(node)                                            # Index attributes

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:                     # Add an edge to the index
        edge_id      = edge.edge_config.edge_id
        from_node_id = edge.from_node_id
        to_node_id   = edge.to_node_id
        edge_type    = edge.edge_type.__name__


        self.index_data.nodes_to_outgoing_edges[from_node_id].add(edge_id)      # Add to node relationship indexes
        self.index_data.nodes_to_incoming_edges[to_node_id].add(edge_id)
        self.index_data.edge_to_nodes[edge_id] = (from_node_id, to_node_id)


        if edge_type not in self.index_data.edges_by_type:                      # Add to type index
            self.index_data.edges_by_type[edge_type] = set()
        self.index_data.edges_by_type[edge_type].add(edge_id)

        self.index_edge_data(edge)                                        # Index edge attributes

    def remove_node(self, node: Schema__MGraph__Node) -> None:  # Remove a node and all its references from the index"""
        node_id = node.node_id

        # Get associated edges before removing node references
        outgoing_edges = self.index_data.nodes_to_outgoing_edges.pop(node_id, set())
        incoming_edges = self.index_data.nodes_to_incoming_edges.pop(node_id, set())

        # Remove from type index
        node_type = node.node_type.__name__
        if node_type in self.index_data.nodes_by_type:
            self.index_data.nodes_by_type[node_type].discard(node_id)
            if not self.index_data.nodes_by_type[node_type]:
                del self.index_data.nodes_by_type[node_type]

        self.remove_node_data(node)                                   # Remove from attribute indexes

    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:          # Remove an edge and all its references from the index
        edge_id = edge.edge_config.edge_id

        if edge_id in self.index_data.edge_to_nodes:
            from_node_id, to_node_id = self.index_data.edge_to_nodes.pop(edge_id)
            self.index_data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
            self.index_data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

        # Remove from type index
        edge_type = edge.edge_type.__name__
        if edge_type in self.index_data.edges_by_type:
            self.index_data.edges_by_type[edge_type].discard(edge_id)
            if not self.index_data.edges_by_type[edge_type]:
                del self.index_data.edges_by_type[edge_type]

        self.remove_edge_data(edge)

    def index_node_data(self, node: Schema__MGraph__Node) -> None:
        """Index all fields from node_data"""
        if node.node_data:
            for field_name, field_value in node.node_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name not in self.index_data.nodes_by_field:
                    self.index_data.nodes_by_field[field_name] = {}
                if field_value not in self.index_data.nodes_by_field[field_name]:
                    self.index_data.nodes_by_field[field_name][field_value] = set()
                self.index_data.nodes_by_field[field_name][field_value].add(node.node_id)

    def remove_node_data(self, node: Schema__MGraph__Node) -> None:
        """Remove indexed node_data fields"""
        if node.node_data:
            for field_name, field_value in node.node_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name in self.index_data.nodes_by_field:
                    if field_value in self.index_data.nodes_by_field[field_name]:
                        self.index_data.nodes_by_field[field_name][field_value].discard(node.node_id)

    def index_edge_data(self, edge: Schema__MGraph__Edge) -> None:
        """Index all fields from edge_data"""
        if edge.edge_data:
            for field_name, field_value in edge.edge_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name not in self.index_data.edges_by_field:
                    self.index_data.edges_by_field[field_name] = {}
                if field_value not in self.index_data.edges_by_field[field_name]:
                    self.index_data.edges_by_field[field_name][field_value] = set()
                self.index_data.edges_by_field[field_name][field_value].add(edge.edge_config.edge_id)

    def remove_edge_data(self, edge: Schema__MGraph__Edge) -> None:
        """Remove indexed edge_data fields"""
        if edge.edge_data:
            for field_name, field_value in edge.edge_data.__dict__.items():
                if field_name.startswith('_'):
                    continue
                if field_name in self.index_data.edges_by_field:
                    if field_value in self.index_data.edges_by_field[field_name]:
                        self.index_data.edges_by_field[field_name][field_value].discard(edge.edge_config.edge_id)

    def load_index_from_graph(self, graph : Domain__MGraph__Graph) -> None:                                             # Create index from existing graph
        for node_id, node in graph.model.data.nodes.items():                                                            # Add all nodes to index
            self.add_node(node)

        for edge_id, edge in graph.model.data.edges.items():                                           # Add all edges to index
            self.add_edge(edge)

    def print_stats(self):
        stats = self.stats()
        pprint(stats)
        return stats

    def save_to_file(self, target_file: str) -> None:                                               # Save index to file
        index_data = self.index_data.json()                                                              # get json (serialised) representation of the index object
        return json_file_create(index_data, target_file)                                            # save it to the target file

    def stats(self) -> Dict[str, Any]:                                                    # Returns statistical summary of index data
        edge_counts = {                                                                                   # Calculate total edges per node
            node_id: {
                'incoming': len(self.index_data.nodes_to_incoming_edges.get(node_id, [])),
                'outgoing': len(self.index_data.nodes_to_outgoing_edges.get(node_id, []))
            }
            for node_id in set(self.index_data.nodes_to_incoming_edges.keys()) |
                           set(self.index_data.nodes_to_outgoing_edges.keys())
        }
        avg_incoming_edges = sum(n['incoming'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0
        avg_outgoing_edges = sum(n['outgoing'] for n in edge_counts.values()) / len(edge_counts) if edge_counts else 0
        stats_data = {                                                                                   # Initialize stats dictionary
            'index_data': {
                'edge_to_nodes'          : len(self.index_data.edge_to_nodes)          ,                # Count of edge to node mappings
                'edges_by_field'         : self.index_data.edges_by_field              ,                # Field indexing for edges
                'edges_by_type'          : {k: len(v) for k,v in                                        # Count of edges per type
                                          self.index_data.edges_by_type.items()}        ,
                'nodes_by_field'         : {                                                            # Counts for field values
                    field_name: { value: len(nodes) for value, nodes in field_values.items()}
                    for field_name, field_values in self.index_data.nodes_by_field.items()
                },
                'nodes_by_type'          : {k: len(v) for k,v in                                        # Count of nodes per type
                                          self.index_data.nodes_by_type.items()}        ,
                'node_edge_connections'   : {                                                           # Consolidated edge counts
                    'total_nodes'        : len(edge_counts)                            ,
                    'avg_incoming_edges' : round(avg_incoming_edges),
                    'avg_outgoing_edges' : round(avg_outgoing_edges),
                    'max_incoming_edges' : max((n['incoming'] for n in edge_counts.values()), default=0),
                    'max_outgoing_edges' : max((n['outgoing'] for n in edge_counts.values()), default=0)
                }
            }
        }

        return stats_data

    # todo: refactor all methods above to MGraph__Index__Create


    ##### getters for data
    # todo refactor this to names like edges__from__node , nodes_from_node

    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all outgoing edges for a node
        return self.index_data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Obj_Id]:           # Get all incoming edges for a node
        return self.index_data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Obj_Id]:      # Get all nodes of a specific type
        return self.index_data.nodes_by_type.get(node_type.__name__, set())

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Obj_Id]:      # Get all edges of a specific type
        return self.index_data.edges_by_type.get(edge_type.__name__, set())

    def get_nodes_by_field(self, field_name: str, field_value: Any) -> Set[Obj_Id]:         # Get all nodes with a specific field value
        return self.index_data.nodes_by_field.get(field_name, {}).get(field_value, set())

    def get_edges_by_field(self, field_name: str, field_value: Any) -> Set[Obj_Id]:         # Get all edges with a specific field value
        return self.index_data.edges_by_field.get(field_name, {}).get(field_value, set())

    # todo: refactor this to something like raw__edges_to_nodes , ...
    #       in fact once we add the main helper methods (like edges_ids__from__node_id) see if these methods are still needed
    def edge_to_nodes           (self): return self.index_data.edge_to_nodes
    def edges_by_field          (self): return self.index_data.edges_by_field
    def edges_by_type           (self): return self.index_data.edges_by_type
    def nodes_by_field          (self): return self.index_data.nodes_by_field
    def nodes_by_type           (self): return self.index_data.nodes_by_type
    def nodes_to_incoming_edges (self): return self.index_data.nodes_to_incoming_edges
    def nodes_to_outgoing_edges (self): return self.index_data.nodes_to_outgoing_edges

    # todo: create this @as_list decorator which converts the return value set to a list (see if that is the better name)
    # @set_to_list
    def edges_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            return list(_.nodes_to_outgoing_edges.get(node_id, {}))         # convert set to list

    def nodes_ids__from__node_id(self, node_id) -> list:
        with self.index_data as _:
            nodes_ids = []
            for edge_id in self.edges_ids__from__node_id(node_id):
                (from_node_id, to_node_id) = _.edge_to_nodes[edge_id]
                nodes_ids.append(to_node_id)
            return nodes_ids



    # todo: see there is a better place to put these static methods (or if we need them to be static)
    @classmethod
    def from_graph(cls, graph: Domain__MGraph__Graph) -> 'MGraph__Index':                           # Create index from graph
        with cls() as _:
            _.load_index_from_graph(graph)                                                             # Build initial index
            return _

    @classmethod
    def from_file(cls, source_file: str) -> 'MGraph__Index':                                           # Load index from file
        with cls() as _:
            index_data   = json_load_file(source_file)
            _.index_data = Schema__MGraph__Index__Data.from_json(index_data)
            return _
