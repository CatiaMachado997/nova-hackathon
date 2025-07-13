#!/usr/bin/env python3
"""
Test script for Cloudera AI Workbench integration
"""

import asyncio
import json
from datetime import datetime

async def test_cloudera_integration():
    """Test the Cloudera integration"""
    
    print("🧪 Testing Cloudera AI Workbench Integration")
    print("=" * 50)
    
    try:
        from agents.cloudera_integration import (
            initialize_cloudera_integration,
            stream_to_cloudera,
            get_cloudera_metrics,
            get_cloudera_analytics
        )
        
        # Test 1: Initialize connection
        print("\n1️⃣ Testing Cloudera connection...")
        connected = await initialize_cloudera_integration()
        if connected:
            print("✅ Cloudera connection successful!")
        else:
            print("❌ Cloudera connection failed!")
            return False
        
        # Test 2: Stream moderation event
        print("\n2️⃣ Testing moderation event streaming...")
        test_event = {
            "task_id": "test-task-123",
            "final_decision": "ALLOW",
            "confidence": 0.95,
            "processing_time": 0.5,
            "individual_responses": {
                "utilitarian": {"decision": "ALLOW", "confidence": 0.9},
                "temporal": {"decision": "ALLOW", "confidence": 0.8}
            },
            "content": "Test content for Cloudera streaming",
            "context": {"platform": "test", "audience_size": 100}
        }
        
        streamed = await stream_to_cloudera("moderation_event", test_event)
        if streamed:
            print("✅ Moderation event streamed successfully!")
        else:
            print("❌ Failed to stream moderation event!")
        
        # Test 3: Get real-time metrics
        print("\n3️⃣ Testing real-time metrics...")
        metrics = await get_cloudera_metrics()
        if "error" not in metrics:
            print("✅ Real-time metrics retrieved!")
            print(f"   Topics: {metrics.get('streaming_topics', 0)}")
            print(f"   Cluster health: {metrics.get('cluster_status', {}).get('cluster_health', 'unknown')}")
        else:
            print(f"❌ Failed to get metrics: {metrics.get('error')}")
        
        # Test 4: Get historical analytics
        print("\n4️⃣ Testing historical analytics...")
        analytics = await get_cloudera_analytics("24h")
        if "error" not in analytics:
            print("✅ Historical analytics retrieved!")
            print(f"   Total moderations: {analytics.get('total_moderations', 0)}")
            print(f"   Time range: {analytics.get('time_range', 'unknown')}")
        else:
            print(f"❌ Failed to get analytics: {analytics.get('error')}")
        
        # Test 5: Stream agent metrics
        print("\n5️⃣ Testing agent metrics streaming...")
        agent_metrics = {
            "agent_name": "TemporalAgent",
            "decision_count": 10,
            "average_confidence": 0.85,
            "response_time_ms": 150,
            "error_count": 0,
            "ethical_framework": "Temporal Ethics",
            "is_active": True
        }
        
        agent_streamed = await stream_to_cloudera("agent_metrics", agent_metrics)
        if agent_streamed:
            print("✅ Agent metrics streamed successfully!")
        else:
            print("❌ Failed to stream agent metrics!")
        
        print("\n" + "=" * 50)
        print("🎉 Cloudera integration test completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

async def test_with_real_data():
    """Test with a real moderation request"""
    
    print("\n🔄 Testing with real moderation data...")
    
    try:
        from agents.cloudera_integration import stream_to_cloudera
        
        # Simulate a real moderation event
        real_event = {
            "task_id": f"real-task-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "final_decision": "FLAG_FOR_REVIEW",
            "confidence": 0.75,
            "processing_time": 1.2,
            "individual_responses": {
                "utilitarian": {"decision": "ALLOW", "confidence": 0.8},
                "deontological": {"decision": "FLAG_FOR_REVIEW", "confidence": 0.7},
                "temporal": {"decision": "FLAG_FOR_REVIEW", "confidence": 0.9},
                "explainability": {"decision": "FLAG_FOR_REVIEW", "confidence": 0.85}
            },
            "content": "This content contains potentially misleading information from 2020 that may not be accurate today.",
            "context": {
                "platform": "social_media",
                "audience_size": 5000,
                "vulnerable_audience": True
            }
        }
        
        success = await stream_to_cloudera("moderation_event", real_event)
        if success:
            print("✅ Real moderation event streamed to Cloudera!")
            print(f"   Task ID: {real_event['task_id']}")
            print(f"   Decision: {real_event['final_decision']}")
            print(f"   Confidence: {real_event['confidence']}")
        else:
            print("❌ Failed to stream real moderation event!")
            
    except Exception as e:
        print(f"❌ Real data test failed: {e}")

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(test_cloudera_integration())
    
    if success:
        # Test with real data
        asyncio.run(test_with_real_data())
    
    print("\n📊 Test Summary:")
    print("   - Check your Cloudera AI Workbench dashboard for streaming data")
    print("   - Look for topics: ethiq.moderation.events, ethiq.agent.metrics")
    print("   - Verify that events are being received in real-time") 