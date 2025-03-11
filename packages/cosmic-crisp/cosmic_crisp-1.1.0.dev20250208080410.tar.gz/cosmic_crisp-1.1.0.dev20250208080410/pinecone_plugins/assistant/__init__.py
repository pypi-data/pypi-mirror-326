from packaging import version
from pinecone_plugin_interface import PluginMetadata
from .assistant import Assistant

try:
    import pinecone
except ImportError as e:
    raise ImportError(
        "This assistant plugin requires the Pinecone SDK to be installed. "
        "Please install the Pinecone SDK by running `pip install pinecone==5.4.2`"
    )

if version.parse(pinecone.__version__) >= version.parse('6.0.0'):
    raise ImportError(
        "This assistant plugin version is not compatible with Pinecone SDK version 6.0.0 or above. "
        "Please downgrade the Pinecone SDK version to 5.4.2 or below by running `pip install pinecone==5.4.2`"
    )

__installables__ = [
    PluginMetadata(
        target_object="Pinecone",
        namespace="assistant",
        implementation_class=Assistant
    ),
]

