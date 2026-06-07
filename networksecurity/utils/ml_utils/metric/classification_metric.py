from networksecurity.entity.artifact_entity import ClassificationReportArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,recall_score,precision_score,accuracy_score
import sys

def get_classification_score(y_true,y_pred) -> ClassificationReportArtifact:
    try:
        model_f1_score = f1_score(y_true=y_true,y_pred=y_pred)
        model_recall_score = recall_score(y_true=y_true,y_pred=y_pred)
        model_precision_score = precision_score(y_true=y_true,y_pred=y_pred)
        model_accuracy_score = accuracy_score(y_true=y_true,y_pred=y_pred)

        classificationArtifact = ClassificationReportArtifact(f1_score=model_f1_score,precision_score=model_precision_score,recall_score=model_recall_score,accuracy_score=model_accuracy_score)
        return classificationArtifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)

