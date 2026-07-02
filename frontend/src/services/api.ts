// api.ts
import type { InputType } from '../components/input/InputSelector';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api/v1' 
    : '/api/v1');

export interface InvestigationReport {
  trust_score: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical' | 'unknown';
  threat_categories: string[];
  summary: string;
  findings: string[];
  confidence: number;
  recommendations: string[];
  detected_pii?: Array<{
    entity_type: string;
    start: number;
    end: number;
    replacement: string;
  }>;
}

export const analyzeContent = async (type: InputType, payload: string | File): Promise<InvestigationReport> => {
  try {
    let contentStr = '';
    
    // For files, we need to convert to base64 if it's an image for our backend,
    // or handle multipart form data. For this capstone demo, assuming we send base64:
    if (type === 'file' && payload instanceof File) {
      contentStr = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(payload);
      });
      // We overwrite the type to 'image' if it's an image to match backend schemas, 
      // but 'file' is used on the frontend for the generic tab.
      if (payload.type.startsWith('image/')) {
        type = 'image' as any;
      }
    } else {
      contentStr = payload as string;
    }

    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content_type: type,
        content: contentStr
      }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data: InvestigationReport = await response.json();
    return data;
  } catch (error) {
    console.error("Analysis API failed:", error);
    throw error;
  }
};
