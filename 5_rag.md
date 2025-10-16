LangChain implements a load of wrapperf for 3rd party tools like dropbox, notion etc.

It uses a cocept called "Document Loader"

# text spliters
splitting chuge chunks of text into chunks


# embeddings
we create a vector space of text. Spaced in relation to their meaning.
Objects added to vector database recive numbers, representing thir place in realation to each other.

When we use vector database. We can first run our query against the database to get vectors nearest to the query (represented also as a vector). And use those nearest vectgors as a context, in the input of the llm