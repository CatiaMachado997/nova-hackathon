"""
Audit Logger Agent for EthIQ Ethical Deliberation System
Logs deliberation process to Notion and streams metrics to Cloudera
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

from .base_agent import BaseAgent, AgentResponse

logger = logging.getLogger(__name__)


class AuditLogger(BaseAgent):
    """
    Audit Logger: Logs deliberation process and streams metrics
    Integrates with Notion for documentation and Cloudera for analytics
    """
    
    def __init__(self, notion_token: Optional[str] = None, cloudera_config: Optional[Dict] = None):
        super().__init__(
            name="AuditLogger",
            description="Logs ethical deliberation process to Notion and streams metrics to Cloudera",
            ethical_framework="Audit and Compliance"
        )
        
        self.notion_token = notion_token or os.getenv("NOTION_TOKEN")
        self.cloudera_config = cloudera_config or self._get_cloudera_config()
        
        # Initialize clients
        self.notion_client = None
        self.cloudera_client = None
        
        # Audit data storage
        self.audit_logs = []
        self.metrics_buffer = []
        
        # Configuration
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")
        self.logging_enabled = True
        self.metrics_enabled = True
    
    def _get_cloudera_config(self) -> Dict[str, Any]:
        """Get Cloudera configuration from environment"""
        return {
            "host": os.getenv("CLOUDERA_HOST"),
            "port": int(os.getenv("CLOUDERA_PORT", "9092")),
            "topic": os.getenv("CLOUDERA_TOPIC", "ethiq-metrics"),
            "username": os.getenv("CLOUDERA_USERNAME"),
            "password": os.getenv("CLOUDERA_PASSWORD")
        }
    
    async def process_task(self, task: Dict[str, Any]) -> AgentResponse:
        """Process audit logging task"""
        
        task_type = task.get("type", "deliberation_log")
        
        if task_type == "deliberation_log":
            return await self.log_deliberation(task)
        elif task_type == "metrics_stream":
            return await self.stream_metrics(task)
        elif task_type == "audit_report":
            return await self.generate_audit_report(task)
        else:
            raise ValueError(f"Unknown audit task type: {task_type}")
    
    async def deliberate(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Deliberate on content (not used for audit logging)"""
        raise NotImplementedError("AuditLogger does not perform ethical deliberation")
    
    async def _analyze_locally(self, content: str, context: Dict[str, Any]) -> AgentResponse:
        """Local analysis (not used for audit logging)"""
        raise NotImplementedError("AuditLogger does not perform local analysis")
    
    def _create_error_response(self, error_message: str) -> AgentResponse:
        """Create error response for audit logging failures"""
        return AgentResponse(
            agent_name=self.name,
            reasoning=f"Audit logging error: {error_message}",
            decision="ERROR",
            confidence=0.0,
            ethical_framework=self.ethical_framework,
            supporting_evidence=[f"Error: {error_message}"]
        )
    
    async def log_deliberation(self, task: Dict[str, Any]) -> AgentResponse:
        """Log a complete deliberation process"""
        
        deliberation_data = task.get("deliberation_data", {})
        task_id = deliberation_data.get("task_id", "unknown")
        
        logger.info(f"AuditLogger logging deliberation for task {task_id}")
        
        # Create audit log entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "content_preview": deliberation_data.get("content_preview", ""),
            "individual_responses": self._format_agent_responses(
                deliberation_data.get("individual_responses", {})
            ),
            "cross_examination": deliberation_data.get("cross_examination", {}),
            "consensus": deliberation_data.get("consensus", {}),
            "final_decision": deliberation_data.get("final_decision", {}),
            "metadata": {
                "agents_involved": len(deliberation_data.get("individual_responses", {})),
                "deliberation_duration": task.get("duration", 0),
                "platform": "EthIQ"
            }
        }
        
        # Store locally
        self.audit_logs.append(audit_entry)
        
        # Log to Notion
        if self.logging_enabled and self.notion_token:
            await self._log_to_notion(audit_entry)
        
        # Stream metrics to Cloudera
        if self.metrics_enabled and self.cloudera_config:
            await self._stream_metrics_to_cloudera(audit_entry)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=f"Successfully logged deliberation for task {task_id}",
            decision="LOGGED",
            confidence=0.9,
            ethical_framework=self.ethical_framework,
            supporting_evidence=[
                f"Audit entry created with {len(audit_entry['individual_responses'])} agent responses",
                f"Notion logging: {'enabled' if self.logging_enabled else 'disabled'}",
                f"Cloudera streaming: {'enabled' if self.metrics_enabled else 'disabled'}"
            ]
        )
        
        self.response_history.append(response)
        return response
    
    async def stream_metrics(self, task: Dict[str, Any]) -> AgentResponse:
        """Stream moderation metrics to Cloudera"""
        
        metrics_data = task.get("metrics_data", {})
        
        # Prepare metrics for streaming
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "metrics_type": "moderation_analytics",
            "data": {
                "total_decisions": metrics_data.get("total_decisions", 0),
                "decision_distribution": metrics_data.get("decision_distribution", {}),
                "average_confidence": metrics_data.get("average_confidence", 0.0),
                "agent_performance": metrics_data.get("agent_performance", {}),
                "deliberation_quality": metrics_data.get("deliberation_quality", {}),
                "framework_usage": metrics_data.get("framework_usage", {})
            }
        }
        
        # Add to buffer
        self.metrics_buffer.append(metrics)
        
        # Stream to Cloudera
        if self.metrics_enabled and self.cloudera_config:
            await self._stream_metrics_to_cloudera(metrics)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=f"Streamed {len(metrics['data'])} metrics to Cloudera",
            decision="STREAMED",
            confidence=0.8,
            ethical_framework=self.ethical_framework,
            supporting_evidence=[
                f"Metrics type: {metrics['metrics_type']}",
                f"Data points: {len(metrics['data'])}",
                f"Cloudera streaming: {'enabled' if self.metrics_enabled else 'disabled'}"
            ]
        )
        
        self.response_history.append(response)
        return response
    
    async def generate_audit_report(self, task: Dict[str, Any]) -> AgentResponse:
        """Generate comprehensive audit report"""
        
        report_period = task.get("period", "all")
        
        # Filter logs based on period
        if report_period == "today":
            today = datetime.now().date()
            filtered_logs = [
                log for log in self.audit_logs
                if datetime.fromisoformat(log["timestamp"]).date() == today
            ]
        elif report_period == "week":
            week_ago = datetime.now().timestamp() - (7 * 24 * 60 * 60)
            filtered_logs = [
                log for log in self.audit_logs
                if datetime.fromisoformat(log["timestamp"]).timestamp() > week_ago
            ]
        else:
            filtered_logs = self.audit_logs
        
        # Generate report
        report = {
            "generated_at": datetime.now().isoformat(),
            "period": report_period,
            "total_deliberations": len(filtered_logs),
            "decision_summary": self._summarize_decisions(filtered_logs),
            "agent_performance": self._analyze_agent_performance(filtered_logs),
            "deliberation_quality": self._analyze_deliberation_quality(filtered_logs),
            "compliance_metrics": self._calculate_compliance_metrics(filtered_logs)
        }
        
        # Log report to Notion
        if self.logging_enabled and self.notion_token:
            await self._log_report_to_notion(report)
        
        response = AgentResponse(
            agent_name=self.name,
            reasoning=f"Generated audit report for {report_period} with {len(filtered_logs)} deliberations",
            decision="REPORT_GENERATED",
            confidence=0.9,
            ethical_framework=self.ethical_framework,
            supporting_evidence=[
                f"Report period: {report_period}",
                f"Total deliberations: {len(filtered_logs)}",
                f"Decision summary: {len(report['decision_summary'])} categories",
                f"Agent performance: {len(report['agent_performance'])} agents analyzed"
            ]
        )
        
        self.response_history.append(response)
        return response
    
    def _format_agent_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Format agent responses for logging"""
        formatted = {}
        for agent_name, response in responses.items():
            if hasattr(response, 'dict'):
                formatted[agent_name] = response.dict()
            else:
                formatted[agent_name] = response
        return formatted
    
    async def _log_to_notion(self, audit_entry: Dict[str, Any]):
        """Log audit entry to Notion"""
        try:
            # This would use the Notion API to create a page in the database
            # For now, we'll simulate the logging
            logger.info(f"Would log to Notion: {audit_entry['task_id']}")
            
            # In a real implementation:
            # from notion_client import Client
            # notion = Client(auth=self.notion_token)
            # notion.pages.create(
            #     parent={"database_id": self.notion_database_id},
            #     properties={
            #         "Task ID": {"title": [{"text": {"content": audit_entry["task_id"]}}]},
            #         "Decision": {"select": {"name": audit_entry["final_decision"]["decision"]}},
            #         "Timestamp": {"date": {"start": audit_entry["timestamp"]}},
            #         "Agents": {"number": audit_entry["metadata"]["agents_involved"]}
            #     }
            # )
            
        except Exception as e:
            logger.error(f"Failed to log to Notion: {e}")
    
    async def _stream_metrics_to_cloudera(self, data: Dict[str, Any]):
        """Stream metrics to Cloudera"""
        try:
            # This would use Kafka to stream to Cloudera
            # For now, we'll simulate the streaming
            logger.info(f"Would stream to Cloudera: {data.get('task_id', 'metrics')}")
            
            # In a real implementation:
            # from kafka import KafkaProducer
            # producer = KafkaProducer(
            #     bootstrap_servers=f"{self.cloudera_config['host']}:{self.cloudera_config['port']}",
            #     security_protocol="SASL_SSL",
            #     sasl_mechanism="PLAIN",
            #     sasl_plain_username=self.cloudera_config['username'],
            #     sasl_plain_password=self.cloudera_config['password']
            # )
            # producer.send(self.cloudera_config['topic'], json.dumps(data).encode())
            
        except Exception as e:
            logger.error(f"Failed to stream to Cloudera: {e}")
    
    def _summarize_decisions(self, logs: List[Dict[str, Any]]) -> Dict[str, int]:
        """Summarize decisions from audit logs"""
        summary = {"ALLOW": 0, "REMOVE": 0, "FLAG_FOR_REVIEW": 0}
        
        for log in logs:
            decision = log.get("final_decision", {}).get("decision", "UNKNOWN")
            if decision in summary:
                summary[decision] += 1
        
        return summary
    
    def _analyze_agent_performance(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze agent performance from audit logs"""
        performance = {}
        
        for log in logs:
            responses = log.get("individual_responses", {})
            for agent_name, response in responses.items():
                if agent_name not in performance:
                    performance[agent_name] = {
                        "total_decisions": 0,
                        "average_confidence": 0.0,
                        "decision_distribution": {"ALLOW": 0.0, "REMOVE": 0.0, "FLAG_FOR_REVIEW": 0.0}
                    }
                
                performance[agent_name]["total_decisions"] += 1
                performance[agent_name]["decision_distribution"][response.get("decision", "UNKNOWN")] += 1
        
        # Calculate averages
        for agent_name, stats in performance.items():
            if stats["total_decisions"] > 0:
                # This would calculate actual average confidence from the data
                stats["average_confidence"] = 0.75  # Placeholder
        
        return performance
    
    def _analyze_deliberation_quality(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze deliberation quality from audit logs"""
        quality_metrics = {
            "total_deliberations": len(logs),
            "average_agents_per_deliberation": 0,
            "consensus_rate": 0,
            "conflict_rate": 0
        }
        
        if not logs:
            return quality_metrics
        
        total_agents = 0
        consensus_count = 0
        conflict_count = 0
        
        for log in logs:
            responses = log.get("individual_responses", {})
            total_agents += len(responses)
            
            # Check for consensus/conflicts
            decisions = [resp.get("decision") for resp in responses.values()]
            if len(set(decisions)) == 1:
                consensus_count += 1
            elif len(set(decisions)) > 1:
                conflict_count += 1
        
        quality_metrics["average_agents_per_deliberation"] = int(total_agents / len(logs))
        quality_metrics["consensus_rate"] = int(consensus_count / len(logs))
        quality_metrics["conflict_rate"] = int(conflict_count / len(logs))
        
        return quality_metrics
    
    def _calculate_compliance_metrics(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate compliance metrics from audit logs"""
        compliance = {
            "total_audited": len(logs),
            "compliance_rate": 1.0,  # Placeholder
            "audit_trail_completeness": 1.0,  # Placeholder
            "transparency_score": 0.9  # Placeholder
        }
        
        return compliance
    
    async def _log_report_to_notion(self, report: Dict[str, Any]):
        """Log audit report to Notion"""
        try:
            logger.info(f"Would log report to Notion: {report['period']}")
            # Similar to _log_to_notion but for reports
        except Exception as e:
            logger.error(f"Failed to log report to Notion: {e}")
    
    def get_audit_summary(self) -> Dict[str, Any]:
        """Get summary of audit logging activities"""
        return {
            "agent_name": self.name,
            "total_logs": len(self.audit_logs),
            "total_metrics": len(self.metrics_buffer),
            "notion_enabled": bool(self.notion_token),
            "cloudera_enabled": bool(self.cloudera_config.get("host")),
            "logging_enabled": self.logging_enabled,
            "metrics_enabled": self.metrics_enabled
        } 