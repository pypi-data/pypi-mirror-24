from trectools import TrecRun
from scipy.stats import norm
import pandas as pd
import numpy as np

class TrecEval:
    def __init__(self, run, qrels):
        self.run = run
        self.qrels = qrels

    def evaluateAll(self):
        pass

    def getReturnedDocuments(self):
        pass

    def getRelevantDocuments(self):
        pass

    def getRunId(self):
        pass

    def getUnjudged(self, depth=10, per_query=False, trec_eval=True):
        label = "UNJ@%ddepth" % (depth)

        if trec_eval:
            trecformat = self.run.run_data.sort_values(["query", "score", "docid"], ascending=[True,False,False]).reset_index()
            topX = trecformat.groupby("query")[["query","docid"]].head(depth)
        else:
            topX = self.run.run_data.groupby("query")[["query","docid"]].head(depth)

        # check number of queries
        nqueries = len(self.run.topics())

        selection = pd.merge(topX, self.qrels.qrels_data[["query","docid","rel"]], how="left")
        selection[label] = selection["rel"].isnull()

        unjX_per_query = selection[["query", label]].groupby("query").sum().astype(np.int) / depth

        if per_query:
            """ This will return a pandas dataframe with ["query", "UNJ@X"] values """
            return unjX_per_query
        return (unjX_per_query.sum() / nqueries)[label]


    def getMAP(self, depth=1000, per_query=False, trec_eval=True):
        label = "MAP@%ddepth" % (depth)

        # We only care for binary evaluation here:
        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0].copy()
        relevant_docs["rel"] = 1

        if trec_eval:
            trecformat = self.run.run_data.sort_values(["query", "score", "docid"], ascending=[True,False,False]).reset_index()
            topX = trecformat.groupby("query")[["query","docid","score"]].head(depth)
        else:
            topX = self.run.run_data.groupby("query")[["query","docid","score"]].head(depth)

        # check number of queries
        nqueries = len(self.run.topics())

        # Make sure that rank position starts by 1
        topX["rank"] = 1
        topX["rank"] = topX.groupby("query")["rank"].cumsum()
        topX["discount"] = 1. / np.log2(topX["rank"]+1)

        # Keep only documents that are relevant (rel > 0)
        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left")

        selection["rel"] = selection.groupby("query")["rel"].cumsum()
        # contribution of each relevant document
        selection[label] = selection["rel"] / selection["rank"]

        # MAP is the sum of individual's contribution
        map_per_query = selection[["query", label]].groupby("query").sum()
        relevant_docs[label] = relevant_docs["rel"]
        nrel_per_query = relevant_docs[["query",label]].groupby("query").sum()
        map_per_query = map_per_query / nrel_per_query

        if per_query:
            """ This will return a pandas dataframe with ["query", "NDCG"] values """
            return map_per_query

        if map_per_query.empty:
            return 0.0

        return (map_per_query.sum() / nqueries)[label]

    def getNDCG(self, depth=1000, per_query=False):
        label = "NDCG@%ddepth" % (depth)

        # Select only topX documents per query
        topX = self.run.run_data.groupby("query")[["query","docid","score"]].head(depth)

        # check number of queries
        nqueries = len(self.qrels.topics())

        # Make sure that rank position starts by 1
        topX["rank"] = 1
        topX["rank"] = topX.groupby("query")["rank"].cumsum()
        topX["discount"] = 1. / np.log2(topX["rank"]+1)

        # Keep only documents that are relevant (rel > 0)
        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0]
        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left")
        selection = selection[~selection["rel"].isnull()]

        # Calculate DCG
        selection[label] = (2**selection["rel"] - 1.0) * selection["discount"]

        # Calculate IDCG
        perfect_ranking = relevant_docs[["query","docid","rel"]].sort_values(["query","rel"], ascending=[True,False])
        perfect_ranking["rank"] = 1
        perfect_ranking["rank"] = perfect_ranking.groupby("query")["rank"].cumsum()
        perfect_ranking["discount"] = 1. / np.log2(perfect_ranking["rank"]+1)
        perfect_ranking[label] = (2**perfect_ranking["rel"] - 1.0) * perfect_ranking["discount"]

        # DCG is the sum of individual's contribution
        dcg_per_query = selection[["query", label]].groupby("query").sum()
        idcg_per_query = perfect_ranking[["query",label]].groupby("query").sum()
        ndcg_per_query = dcg_per_query / idcg_per_query

        if per_query:
            """ This will return a pandas dataframe with ["query", "NDCG"] values """
            return ndcg_per_query

        if ndcg_per_query.empty:
            return 0.0

        return (ndcg_per_query.sum() / nqueries)[label]

    def getPrecisionAtDepth(self, depth=10, per_query=False, trec_eval=True, removeUnjudged=False):
        label = "P@%d" % (depth)

        # check number of queries
        nqueries = len(self.qrels.topics())

        qrels = self.qrels.qrels_data
        run = self.run.run_data

        merged = pd.merge(run, qrels[["query","docid","rel"]], how="left")

        if trec_eval:
            merged.sort_values(["query", "score", "docid"], ascending=[True,False,False], inplace=True)

        if removeUnjudged:
            merged = merged[~merged.rel.isnull()]

        topX = merged.groupby("query")[["query","docid","rel"]].head(depth)
        topX[label] = topX["rel"] > 0
        pX_per_query = topX[["query", label]].groupby("query").sum().astype(np.int) / depth

        if per_query:
            """ This will return a pandas dataframe with ["query", "P@X"] values """
            return pX_per_query
        return (pX_per_query.sum() / nqueries)[label]


    def getPrecisionAtXold(self, X=10, per_query=False, trec_eval=True):
        # Whenever I have the time, I should check if I can delete this function
        label = "P@%d" % (X)

        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0]

        if trec_eval:
            trecformat = self.run.run_data.sort_values(["query", "score", "docid"], ascending=[True,False,False]).reset_index()
            topX = trecformat.groupby("query")[["query","docid"]].head(X)
        else:
            topX = self.run.run_data.groupby("query")[["query","docid"]].head(X)

        # check number of queries
        nqueries = len(self.qrels.topics())

        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left")
        selection[label] = ~selection["rel"].isnull()

        pX_per_query = selection[["query", label]].groupby("query").sum().astype(np.int) / X

        if per_query:
            """ This will return a pandas dataframe with ["query", "P@X"] values """
            return pX_per_query
        return (pX_per_query.sum() / nqueries)[label]

    def getRBP(self, p=0.8, depth=1000, per_query=False, binary_topical_relevance=True, average_ties=True):
        """
        """
        label = "RBP(%.2f)@%ddepth" % (p, depth)

        # Select only topX documents per query
        topX = self.run.run_data.groupby("query")[["query","docid","score"]].head(depth)

        # check number of queries
        nqueries = len(self.run.topics())

        # Make sure that rank position starts by 1
        topX["rank"] = 1
        topX["rank"] = topX.groupby("query")["rank"].cumsum()

        # Calculate RBP based on rank of documents
        topX[label] = (1.0-p) * (p) ** (topX["rank"]-1)

        # Average ties if required:
        if average_ties:
            topX["score+1"] = topX["score"].shift(1)
            topX["ntie"] = topX["score"] != topX["score+1"]
            topX["grps"] = topX["ntie"].cumsum()
            averages = topX[[label,"grps"]].groupby("grps")[label].mean().reset_index().rename(columns={label: "avgs"})
            topX = pd.merge(averages, topX)
            topX[label] = topX["avgs"]
            for k in ["score","score+1","ntie","grps","avgs"]:
                del topX[k]

        # Keep only documents that are relevant (rel > 0)
        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0]
        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left")
        selection = selection[~selection["rel"].isnull()]

        if not binary_topical_relevance:
            selection[label] = selection[label] * selection["rel"]

        # RBP is the sum of individual's contribution
        rbp_per_query = selection[["query", label]].groupby("query").sum()

        if per_query:
            """ This will return a pandas dataframe with ["query", "RBP"] values """
            return rbp_per_query

        if rbp_per_query.empty:
            return 0.0

        return (rbp_per_query.sum() / nqueries)[label]

    def getURBP(self, additional_qrel, strategy="direct_multiplication", normalization_factor = 1.0, p=0.8, depth=1000, per_query=False, binary_topical_relevance=True, average_ties=True):
        """
            uRBP is the modification of RBP to cope with other dimentions of relevation.
            The important parameters are:
                * p: same as RBP(p)
                * depth: the depth per topic/query that we should look at when evaluation
                * strategy: one of:
                    - direct_multiplication: simply will multiply the RBP value of a document by the additional_qrel["rel"] for that document
                    - TODO (dictionary transformation)
                * normalization_factor: a value which will be multiplied to the addtional_qrel["rel"] value. Use it to transform a 0-1 scale into a 0-100 (with normalization_factor = 100). Default: 1.0

        """

        label = "uRBP(%.2f)@%ddepth" % (p, depth)

        # Select only topX documents per query
        topX = self.run.run_data.groupby("query")[["query","docid","score"]].head(depth)

        # check number of queries
        nqueries = len(self.qrels.topics())

        # Make sure that rank position starts by 1
        topX["rank"] = 1
        topX["rank"] = topX.groupby("query")["rank"].cumsum()

        # Calculate RBP based on rank of documents
        topX[label] = (1.0-p) * (p) ** (topX["rank"]-1)

        # Average ties if required:
        if average_ties:
            topX["score+1"] = topX["score"].shift(1)
            topX["ntie"] = topX["score"] != topX["score+1"]
            topX["grps"] = topX["ntie"].cumsum()
            averages = topX[[label,"grps"]].groupby("grps")[label].mean().reset_index().rename(columns={label: "avgs"})
            topX = pd.merge(averages, topX)
            topX[label] = topX["avgs"]
            for k in ["score","score+1","ntie","grps","avgs"]:
                del topX[k]

        # Keep only documents that are relevant (rel > 0)
        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0]
        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left").\
                                merge(additional_qrel.qrels_data, on=["query","docid"], suffixes=("","_other"))
        selection = selection[~selection["rel"].isnull()]

        if strategy == "direct_multiplication":
            selection[label] = selection[label] * selection["rel_other"] * normalization_factor

        if not binary_topical_relevance:
            selection[label] = selection[label] * selection["rel"]

        # RBP is the sum of individual's contribution
        rbp_per_query = selection[["query", label]].groupby("query").sum()

        if per_query:
            """ This will return a pandas dataframe with ["query", "RBP"] values """
            return rbp_per_query

        if rbp_per_query.empty:
            return 0.0

        return (rbp_per_query.sum() / nqueries)[label]


    def getAlphaURBP(self, additional_qrel, goals, strategy="direct_multiplication", normalization_factor = 1.0, p=0.8, depth=1000, per_query=False, binary_topical_relevance=True, average_ties=True):

        """
            alphaURBP is the modification of uRBP to cope with various profiles defined using alpha.
            The important parameters are:
                * p: same as RBP(p)
                * depth: the depth per topic/query that we should look at when evaluation
                * goals: a dictionary like {query: [goal,var]}
                * strategy: one of:
                    - direct_multiplication: simply will multiply the RBP value of a document by the additional_qrel["rel"] for that document
                    - TODO (dictionary transformation)
                * normalization_factor: a value which will be multiplied to the addtional_qrel["rel"] value. Use it to transform a 0-1 scale into a 0-100 (with normalization_factor = 100). Default: 1.0

        """

        label = "auRBP(%.2f)@%ddepth" % (p, depth)

        # Select only topX documents per query
        topX = self.run.run_data.groupby("query")[["query","docid","score"]].head(depth)

        # check number of queries
        nqueries = len(self.qrels.topics())

        # Make sure that rank position starts by 1
        topX["rank"] = 1
        topX["rank"] = topX.groupby("query")["rank"].cumsum()

        # Calculate RBP based on rank of documents
        topX[label] = (1.0-p) * (p) ** (topX["rank"]-1)

        # Average ties if required:
        if average_ties:
            topX["score+1"] = topX["score"].shift(1)
            topX["ntie"] = topX["score"] != topX["score+1"]
            topX["grps"] = topX["ntie"].cumsum()
            averages = topX[[label,"grps"]].groupby("grps")[label].mean().reset_index().rename(columns={label: "avgs"})
            topX = pd.merge(averages, topX)
            topX[label] = topX["avgs"]
            for k in ["score","score+1","ntie","grps","avgs"]:
                del topX[k]

        # Keep only documents that are relevant (rel > 0)
        relevant_docs = self.qrels.qrels_data[self.qrels.qrels_data.rel > 0]
        selection = pd.merge(topX, relevant_docs[["query","docid","rel"]], how="left").\
                                merge(additional_qrel.qrels_data, on=["query","docid"], suffixes=("","_other"))
        selection = selection[~selection["rel"].isnull()]

        # Transform dictionary into dataframe
        goals = pd.DataFrame.from_dict(goals, orient='index').reset_index()
        goals.columns = ["query", "mean", "var"]

        def normvalue(value, goal, var):
            return norm.pdf(value, goal, var) * 100. / norm.pdf(goal, goal, var)

        # TODO: now I am forcing the queries to be integer. Need to find a better way to cope with different data types
        selection["query"] = selection["query"].astype(np.int)
        goals["query"] = goals["query"].astype(np.int)

        selection = pd.merge(selection, goals)
        selection["rel_other"] = selection[["rel_other", "mean", "var"]].\
                                    apply(lambda x: normvalue(x["rel_other"], x["mean"], x["var"]), axis=1)

        if strategy == "direct_multiplication":
            selection[label] = selection[label] * selection["rel_other"] * normalization_factor

        if not binary_topical_relevance:
            selection[label] = selection[label] * selection["rel"]

        # RBP is the sum of individual's contribution
        rbp_per_query = selection[["query", label]].groupby("query").sum()

        if per_query:
            """ This will return a pandas dataframe with ["query", "RBP"] values """
            return rbp_per_query

        if rbp_per_query.empty:
            return 0.0

        return (rbp_per_query.sum() / nqueries)[label]


