"""Tests for agent modules"""

import pytest
from src.agents.base import BaseAgent
from src.agents.research import ResearchAgent
from src.agents.document import DocumentAgent
from src.agents.general import GeneralAgent
from src.agents.code import CodeAgent
from src.config import config


def test_base_agent_instantiation():
    """Test BaseAgent can be instantiated"""
    agent = BaseAgent()
    assert agent is not None
    assert hasattr(agent, 'build_prompt')
    assert hasattr(agent, 'build_executor')
    assert hasattr(agent, 'run')


def test_research_agent_instantiation():
    """Test ResearchAgent can be instantiated"""
    agent = ResearchAgent()
    assert agent is not None
    assert isinstance(agent, BaseAgent)


def test_document_agent_instantiation():
    """Test DocumentAgent can be instantiated"""
    agent = DocumentAgent()
    assert agent is not None
    assert isinstance(agent, BaseAgent)


def test_general_agent_instantiation():
    """Test GeneralAgent can be instantiated"""
    agent = GeneralAgent()
    assert agent is not None
    assert isinstance(agent, BaseAgent)


def test_code_agent_instantiation():
    """Test CodeAgent can be instantiated"""
    agent = CodeAgent()
    assert agent is not None
    assert isinstance(agent, BaseAgent)


def test_config_loaded():
    """Test config is properly loaded"""
    assert config.groq_api_key is not None
    assert config.model_name == "llama-3.3-70b-versatile"
    assert config.temperature == 0.7
    assert config.max_tokens == 2048
