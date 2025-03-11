import requests
from typing import Dict, Optional, Any
import pandas as pd
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from .exceptions import KruncherAuthError

@dataclass
class KruncherClientBuilder:
    api_key: Optional[str] = None

    def build(self) -> 'KruncherClient':
        return KruncherClient(api_key=self.api_key)

class KruncherClient:
    """Client for interacting with the Kruncher API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Kruncher client.
        
        Args:
            api_key: Optional API key. If not provided, will try to load from environment
                    variable KRUNCHER_API_KEY
        
        Raises:
            KruncherAuthError: If no API key is found
        """
        self.BASE_URL = "https://api.kruncher.ai"
        
        # Try to get API key from argument or environment
        self.api_key = api_key if api_key else self._get_api_key()
        
        if not self.api_key:
            raise KruncherAuthError(
                "No API key provided. Either pass api_key to KruncherClient "
                "or set KRUNCHER_API_KEY environment variable"
            )
        
        # Set up session with auth
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        })

    def _get_api_key(self) -> Optional[str]:
        """Try to load API key from environment variables."""
        # Try to load from .env file
        load_dotenv()
        return os.getenv('KRUNCHER_API_KEY')

    def get_projects(self, page: int = 0) -> Dict[str, Any]:
        """
        Get projects with pagination.
        
        Args:
            page: Page number (0-based)
            
        Returns:
            Dict containing the response data and pagination information
        """
        get_project_url = f"{self.BASE_URL}/api/integration/projects"
        response = self._session.get(
            get_project_url,
            params={
                "page": page
            }
        )
        response.raise_for_status()
        return response.json()

    def get_projects_df(self, page: int = 0) -> pd.DataFrame:
        """
        Get projects as a pandas DataFrame.
        
        Args:
            page: Page number (0-based)
            
        Returns:
            DataFrame containing the projects data with key company information
            and the last analysis ID for each project
        """
        response = self.get_projects(page)
        
        # Extract projects from response
        projects = response.get('data', [])
        
        # Define the columns we want to extract
        columns = [
            'id', 'name', 'companyName', 'companyLegalName', 'companyWebsite',
            'companyIndustry', 'companyCountry', 'companyBusinessModel',
            'companyStage', 'companyRevenueRange', 'companySummary',
            'companyKeywordSummary', 'processing'
        ]
        
        # Create list to store project data with analysis ID
        project_data = []
        for project in projects:
            # Get basic project data
            data = {col: project.get(col) for col in columns}
            
            # Add last analysis ID if available
            analyses = project.get('analyses', [])
            data['last_analysis_id'] = analyses[0].get('id') if analyses else None
            
            project_data.append(data)
        
        # Create DataFrame with all data
        df = pd.DataFrame(project_data)
        
        # Add pagination info as DataFrame attributes
        df.attrs['pagination'] = response.get('pagination', {})
        
        return df

    def get_analysis_detail(self, analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis details by ID.
        
        Args:
            analysis_id: The ID of the analysis to retrieve
            
        Returns:
            Dict containing the analysis details
        """
        response = self._session.get(
            f"{self.BASE_URL}/api/integration/analysis/detail",
            params={"analysisId": analysis_id}
        )
        response.raise_for_status()
        return response.json()

    def get_analysis_detail_df(self, analysis_id: str) -> Dict[str, pd.DataFrame]:
        """
        Get analysis details as a collection of pandas DataFrames.
        
        Args:
            analysis_id: The ID of the analysis to retrieve
            
        Returns:
            Dictionary containing multiple DataFrames for different aspects of the analysis:
            - main_info: Basic company information
            - founders: Founders' information
            - competitors: Competitor analysis
            - news: News articles
            - funding_history: Funding rounds
            - investors: Investor information
        """
        response = self.get_analysis_detail(analysis_id)
        analysis_data = response.get('data', {}).get('analysisData', {})
        
        # Create main information DataFrame
        main_info = pd.DataFrame([{
            'companyName': analysis_data.get('companyName', {}).get('text'),
            'companyLegalName': analysis_data.get('companyLegalName', {}).get('text'),
            'website': analysis_data.get('website', {}).get('text'),
            'foundYear': analysis_data.get('foundYear', {}).get('dataPoint', {}).get('integerValue'),
            'numberOfEmployees': analysis_data.get('numberOfEmployees', {}).get('dataPoint', {}).get('integerValue'),
            'officeLocation': analysis_data.get('officeLocation', {}).get('text'),
            'companySummary': analysis_data.get('companySummary', {}).get('text'),
            'keywordSummary': analysis_data.get('keywordSummary', {}).get('text'),
            'cagr': analysis_data.get('cagr', {}).get('text'),
            'som': analysis_data.get('som', {}).get('text'),
        }])

        # Create founders DataFrame
        founders_data = response.get('founders', [])
        founders_df = pd.DataFrame(founders_data)

        # Create competitors DataFrame
        competitors_data = analysis_data.get('competitorStructured', {}).get('structuredData', [])
        competitors_df = pd.DataFrame(competitors_data)

        # Create news DataFrame
        news_data = analysis_data.get('newsStructured', {}).get('structuredData', [])
        news_df = pd.DataFrame(news_data)

        # Create funding history DataFrame
        funding_data = analysis_data.get('history', {}).get('structuredData', [])
        funding_df = pd.DataFrame([{
            'round_type': round.get('investment_type_label'),
            'amount': round.get('money_raised'),
            'date': round.get('closed_on'),
            'num_investors': round.get('num_investors'),
            'stage': round.get('funding_stage_label')
        } for round in funding_data])

        # Create investors DataFrame
        investors = []
        for round in funding_data:
            for investor in round.get('investor_breakdown', []):
                investors.append({
                    'name': investor.get('name'),
                    'type': investor.get('type'),
                    'image_url': investor.get('image_url'),
                    'permalink': investor.get('permalink'),
                    'round_type': round.get('investment_type_label'),
                    'round_date': round.get('closed_on')
                })
        investors_df = pd.DataFrame(investors)

        return {
            'main_info': main_info,
            'founders': founders_df,
            'competitors': competitors_df,
            'news': news_df,
            'funding_history': funding_df,
            'investors': investors_df
        } 
    
    def get_projects_df_full(self, page: int = 0) -> pd.DataFrame:
        """
        Get ALL projects data as a fully flattened pandas DataFrame.
        
        This method uses pd.json_normalize to flatten every key from the JSON response.
        The pagination info is attached as a DataFrame attribute.
        """
        response = self.get_projects(page)
        projects = response.get('data', [])
        # Use json_normalize to flatten nested structures (using "_" as separator)
        df = pd.json_normalize(projects, sep='_')
        df.attrs['pagination'] = response.get('pagination', {})
        return df

    
    def get_analysis_df_full(self, analysis_id: str) -> pd.DataFrame:
        """
        Get ALL analysis details as a single flattened pandas DataFrame.
        
        This method flattens the entire JSON response (including metadata and nested data)
        using pd.json_normalize.
        """
        response = self.get_analysis_detail(analysis_id)
        # Flatten the entire response; nested keys will be separated by '_'
        df = pd.json_normalize(response, sep='_')
        return df