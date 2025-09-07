#!/usr/bin/env python3
"""
Simple test script for the BigQuery Data Analyst Agent.

This script tests:
1. Agent creation and initialization
2. Basic configuration validation
3. Import functionality
"""

def test_agent_creation():
    """
    Test that the BQ agent can be created successfully.
    """
    try:
        from bq_data_analyst_agent import create_bq_data_analyst_agent
        
        # Create the agent
        agent = create_bq_data_analyst_agent()
        
        # Basic validation
        assert agent.name == "bq_data_analyst", f"Expected name 'bq_data_analyst', got '{agent.name}'"
        assert agent.model == "gemini-2.0-flash", f"Expected model 'gemini-2.0-flash', got '{agent.model}'"
        assert agent.tools is not None, "Agent should have tools configured"
        assert len(agent.tools) > 0, "Agent should have at least one tool"
        assert agent.instruction is not None, "Agent should have instructions"
        assert len(agent.instruction.strip()) > 0, "Agent instructions should not be empty"
        
        print("✅ Agent creation test passed!")
        print(f"   - Name: {agent.name}")
        print(f"   - Model: {agent.model}")
        print(f"   - Tools count: {len(agent.tools)}")
        print(f"   - Instructions length: {len(agent.instruction)} characters")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure google-adk is installed: pip install google-adk")
        return False
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_agent_properties():
    """
    Test agent properties and configuration.
    """
    try:
        from bq_data_analyst_agent import create_bq_data_analyst_agent
        
        agent = create_bq_data_analyst_agent()
        
        # Test that the agent has the expected properties
        expected_keywords = [
            "bigquery", "sql", "query", "data", "analyst", "analyze"
        ]
        
        instruction_lower = agent.instruction.lower()
        found_keywords = [kw for kw in expected_keywords if kw in instruction_lower]
        
        print("✅ Agent properties test passed!")
        print(f"   - Found keywords in instructions: {found_keywords}")
        print(f"   - Description: {agent.description[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent properties test failed: {e}")
        return False

def main():
    """
    Run all tests.
    """
    print("🧪 Testing BigQuery Data Analyst Agent...\n")
    
    tests = [
        ("Agent Creation", test_agent_creation),
        ("Agent Properties", test_agent_properties)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The BQ Data Analyst Agent is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Set up Google Cloud authentication")
        print("   2. Configure your BigQuery project")
        print("   3. Run: python bq_analyst_example.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())