from knowledge.knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader()

context = loader.build_context(
    "My ration card application has been pending for four months."
)

print(context)