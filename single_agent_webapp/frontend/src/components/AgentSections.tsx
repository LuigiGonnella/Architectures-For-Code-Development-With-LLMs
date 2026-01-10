import React from 'react';

interface AnalysisSectionProps {
  content: string;
}

export const AnalysisSection: React.FC<AnalysisSectionProps> = ({ content }) => {
  // Extract key sections from analysis
  const sections = {
    requiredBehavior: extractSection(content, 'Required Behavior', 'Inputs and Outputs'),
    inputsOutputs: extractSection(content, 'Inputs and Outputs', 'Constraints'),
    constraints: extractSection(content, 'Constraints', 'Edge Cases'),
    edgeCases: extractSection(content, 'Edge Cases', 'Ambiguities'),
  };

  return (
    <div className="space-y-4 bg-gradient-to-br from-slate-800/40 to-slate-900/40 p-4 rounded-lg border border-slate-700/50">
      <div className="flex items-center gap-2 text-sky-400 font-bold text-lg">
        <span>📊</span>
        <span>Analysis</span>
      </div>
      
      {sections.requiredBehavior && (
        <div className="pl-4 space-y-2">
          <h4 className="text-sm font-bold text-sky-300 uppercase tracking-wide">Required Behavior</h4>
          <p className="text-base text-slate-100 leading-relaxed font-medium">{sections.requiredBehavior.trim()}</p>
        </div>
      )}
      
      {sections.edgeCases && (
        <div className="pl-4 space-y-2">
          <h4 className="text-sm font-bold text-sky-300 uppercase tracking-wide">Edge Cases</h4>
          <p className="text-base text-slate-100 leading-relaxed font-medium whitespace-pre-line">{sections.edgeCases.trim()}</p>
        </div>
      )}
    </div>
  );
};

interface PlanSectionProps {
  content: string;
}

export const PlanSection: React.FC<PlanSectionProps> = ({ content }) => {
  // Extract approach and complexity
  const approach = extractSection(content, 'High-Level Approach', 'Step-by-Step Plan') || 
                   extractSection(content, 'High-Level Approach', 'Edge Case Handling');
  const complexity = extractComplexity(content);

  return (
    <div className="space-y-4 bg-gradient-to-br from-violet-900/20 to-purple-900/20 p-4 rounded-lg border border-violet-700/50">
      <div className="flex items-center gap-2 text-violet-400 font-bold text-lg">
        <span>📝</span>
        <span>Solution Plan</span>
      </div>
      
      {approach && (
        <div className="pl-4">
          <p className="text-base text-slate-100 leading-relaxed font-medium">{approach.trim()}</p>
        </div>
      )}
      
      {complexity && (
        <div className="pl-4 mt-3 bg-gradient-to-br from-amber-900/30 to-orange-900/30 rounded-xl p-5 border-2 border-amber-600/60 shadow-lg">
          <h4 className="text-lg font-bold text-amber-300 mb-4 flex items-center gap-2">
            <span className="text-xl">⚡</span>
            <span>COMPLEXITY ANALYSIS</span>
          </h4>
          <div className="space-y-3">
            {complexity.time && (
              <div className="flex items-center gap-4 bg-gradient-to-r from-emerald-900/40 to-green-900/40 rounded-lg p-3 border border-emerald-600/50">
                <span className="text-emerald-300 font-bold text-base">⏱️ Time:</span>
                <code className="text-emerald-200 font-mono text-lg font-bold tracking-wide">{complexity.time}</code>
              </div>
            )}
            {complexity.space && (
              <div className="flex items-center gap-4 bg-gradient-to-r from-blue-900/40 to-cyan-900/40 rounded-lg p-3 border border-blue-600/50">
                <span className="text-blue-300 font-bold text-base">💾 Space:</span>
                <code className="text-blue-200 font-mono text-lg font-bold tracking-wide">{complexity.space}</code>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper functions
function extractSection(content: string, startMarker: string, endMarker: string): string | null {
  const startIdx = content.indexOf(startMarker);
  if (startIdx === -1) return null;
  
  const contentAfterStart = content.substring(startIdx + startMarker.length);
  const endIdx = contentAfterStart.indexOf(endMarker);
  
  if (endIdx === -1) {
    return contentAfterStart.trim();
  }
  
  return contentAfterStart.substring(0, endIdx).trim();
}

function extractComplexity(content: string): { time?: string; space?: string } | null {
  // Search the entire content for complexity information
  const timeMatch = content.match(/Time Complexity:\s*([^\n.]+(?:\([^)]+\))?)/i) ||
                   content.match(/time:\s*([OΘΩo]\([^)]+\))/i);
  const spaceMatch = content.match(/Space Complexity:\s*([^\n.]+(?:\([^)]+\))?)/i) ||
                    content.match(/space:\s*([OΘΩo]\([^)]+\))/i);
  
  if (!timeMatch && !spaceMatch) return null;
  
  return {
    time: timeMatch ? timeMatch[1].trim() : undefined,
    space: spaceMatch ? spaceMatch[1].trim() : undefined,
  };
}
