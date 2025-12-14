"""
Security Calculator Service - Assesses security posture and generates scores
"""
from typing import Dict, List
from pydantic import BaseModel


class AssessmentResponse(BaseModel):
    """User's assessment responses"""
    answers: Dict[str, bool]
    industry: str
    company_size: str


class SecurityCalculator:
    """Service for calculating security scores and benchmarking"""
    
    def __init__(self):
        self.questions = self._load_questions()
        self.benchmarks = self._load_benchmarks()
    
    def _load_questions(self) -> Dict[str, List[Dict]]:
        """Load assessment questions by category"""
        return {
            "access_control": [
                {
                    "id": "ac1",
                    "question": "Do you enforce multi-factor authentication (MFA) for all users?",
                    "weight": 10
                },
                {
                    "id": "ac2",
                    "question": "Do you have role-based access control (RBAC) implemented?",
                    "weight": 8
                },
                {
                    "id": "ac3",
                    "question": "Do you regularly review and revoke unnecessary access permissions?",
                    "weight": 7
                },
                {
                    "id": "ac4",
                    "question": "Do you use single sign-on (SSO) for application access?",
                    "weight": 6
                }
            ],
            "data_protection": [
                {
                    "id": "dp1",
                    "question": "Is all sensitive data encrypted at rest?",
                    "weight": 10
                },
                {
                    "id": "dp2",
                    "question": "Is all data encrypted in transit (TLS/SSL)?",
                    "weight": 10
                },
                {
                    "id": "dp3",
                    "question": "Do you have a data classification policy in place?",
                    "weight": 7
                },
                {
                    "id": "dp4",
                    "question": "Do you perform regular data backups?",
                    "weight": 8
                }
            ],
            "network_security": [
                {
                    "id": "ns1",
                    "question": "Do you have a firewall protecting your network perimeter?",
                    "weight": 9
                },
                {
                    "id": "ns2",
                    "question": "Do you use network segmentation to isolate sensitive systems?",
                    "weight": 8
                },
                {
                    "id": "ns3",
                    "question": "Do you have intrusion detection/prevention systems (IDS/IPS)?",
                    "weight": 7
                },
                {
                    "id": "ns4",
                    "question": "Do you monitor network traffic for anomalies?",
                    "weight": 7
                }
            ],
            "incident_response": [
                {
                    "id": "ir1",
                    "question": "Do you have a documented incident response plan?",
                    "weight": 9
                },
                {
                    "id": "ir2",
                    "question": "Do you conduct regular incident response drills?",
                    "weight": 7
                },
                {
                    "id": "ir3",
                    "question": "Do you have 24/7 security monitoring?",
                    "weight": 8
                },
                {
                    "id": "ir4",
                    "question": "Do you maintain audit logs for security events?",
                    "weight": 8
                }
            ],
            "compliance": [
                {
                    "id": "cm1",
                    "question": "Do you comply with relevant industry regulations (SOC 2, ISO 27001, GDPR, etc.)?",
                    "weight": 10
                },
                {
                    "id": "cm2",
                    "question": "Do you conduct regular compliance audits?",
                    "weight": 8
                },
                {
                    "id": "cm3",
                    "question": "Do you have documented security policies and procedures?",
                    "weight": 7
                },
                {
                    "id": "cm4",
                    "question": "Do you track and remediate compliance gaps?",
                    "weight": 7
                }
            ],
            "security_awareness": [
                {
                    "id": "sa1",
                    "question": "Do you provide regular security awareness training to employees?",
                    "weight": 8
                },
                {
                    "id": "sa2",
                    "question": "Do you conduct phishing simulation exercises?",
                    "weight": 7
                },
                {
                    "id": "sa3",
                    "question": "Do you have a security champion program?",
                    "weight": 6
                },
                {
                    "id": "sa4",
                    "question": "Do you have a clear security incident reporting process?",
                    "weight": 8
                }
            ]
        }
    
    def _load_benchmarks(self) -> Dict[str, Dict[str, int]]:
        """Load industry benchmark data"""
        return {
            "fintech": {
                "access_control": 85,
                "data_protection": 90,
                "network_security": 82,
                "incident_response": 80,
                "compliance": 95,
                "security_awareness": 75
            },
            "healthcare": {
                "access_control": 80,
                "data_protection": 95,
                "network_security": 78,
                "incident_response": 82,
                "compliance": 92,
                "security_awareness": 70
            },
            "saas": {
                "access_control": 82,
                "data_protection": 85,
                "network_security": 80,
                "incident_response": 78,
                "compliance": 75,
                "security_awareness": 72
            },
            "ecommerce": {
                "access_control": 75,
                "data_protection": 88,
                "network_security": 76,
                "incident_response": 70,
                "compliance": 80,
                "security_awareness": 68
            },
            "general": {
                "access_control": 70,
                "data_protection": 75,
                "network_security": 72,
                "incident_response": 65,
                "compliance": 70,
                "security_awareness": 60
            }
        }
    
    def calculate_score(self, responses: AssessmentResponse) -> Dict:
        """
        Calculate security score based on responses
        
        Returns:
            Dictionary with overall score, category scores, and radar chart data
        """
        category_scores = {}
        
        for category, questions in self.questions.items():
            total_weight = sum(q["weight"] for q in questions)
            earned_points = sum(
                q["weight"] for q in questions 
                if responses.answers.get(q["id"], False)
            )
            
            # Calculate percentage score
            score = round((earned_points / total_weight) * 100, 1) if total_weight > 0 else 0
            category_scores[category] = score
        
        # Calculate overall score (weighted average)
        overall_score = round(sum(category_scores.values()) / len(category_scores), 1)
        
        # Get benchmark data
        benchmark = self.get_benchmark_data(responses.industry)
        
        # Generate radar chart data
        radar_data = self.generate_radar_chart_data(category_scores, benchmark)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(category_scores)
        
        return {
            "overall_score": overall_score,
            "category_scores": category_scores,
            "radar_data": radar_data,
            "benchmark": benchmark,
            "recommendations": recommendations,
            "grade": self._get_grade(overall_score)
        }
    
    def get_benchmark_data(self, industry: str) -> Dict[str, int]:
        """Get industry benchmark for comparison"""
        return self.benchmarks.get(industry.lower(), self.benchmarks["general"])
    
    def generate_radar_chart_data(self, scores: Dict[str, float], benchmark: Dict[str, int]) -> Dict:
        """Format data for radar chart visualization"""
        categories = [
            "Access Control",
            "Data Protection",
            "Network Security",
            "Incident Response",
            "Compliance",
            "Security Awareness"
        ]
        
        category_keys = [
            "access_control",
            "data_protection",
            "network_security",
            "incident_response",
            "compliance",
            "security_awareness"
        ]
        
        return {
            "labels": categories,
            "scores": [scores.get(key, 0) for key in category_keys],
            "benchmark": [benchmark.get(key, 0) for key in category_keys]
        }
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[Dict]:
        """Generate recommendations based on scores"""
        recommendations = []
        
        for category, score in scores.items():
            if score < 60:
                priority = "HIGH"
                message = f"Critical gaps in {category.replace('_', ' ').title()}. Immediate action required."
            elif score < 75:
                priority = "MEDIUM"
                message = f"Improvement needed in {category.replace('_', ' ').title()}."
            else:
                priority = "LOW"
                message = f"{category.replace('_', ' ').title()} is well-managed. Continue monitoring."
            
            recommendations.append({
                "category": category.replace('_', ' ').title(),
                "score": score,
                "priority": priority,
                "message": message
            })
        
        # Sort by priority (HIGH first)
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        recommendations.sort(key=lambda x: priority_order[x["priority"]])
        
        return recommendations
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def get_all_questions(self) -> Dict[str, List[Dict]]:
        """Return all questions for the assessment"""
        return self.questions
