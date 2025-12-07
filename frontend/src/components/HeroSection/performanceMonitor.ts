// Simple performance monitoring for asset loading times
export const measureAssetLoadTime = (url: string, callback: (loadTime: number) => void): void => {
  const startTime = performance.now();

  const img = new Image();
  img.onload = () => {
    const loadTime = performance.now() - startTime;
    callback(loadTime);
  };

  img.onerror = () => {
    const loadTime = performance.now() - startTime;
    callback(loadTime); // Still report the time even if there was an error
  };

  // Add a cache buster to get accurate measurements
  img.src = `${url}?t=${Date.now()}`;
};

// Monitor overall page performance
export const measurePageLoadTime = (): number | null => {
  if (performance.timing && performance.timing.navigationStart) {
    return performance.now();
  }
  return null;
};

// Log performance metrics
export const logPerformanceMetrics = (componentName: string, metrics: Record<string, any>): void => {
  if (process.env.NODE_ENV === 'development') {
    console.group(`Performance Metrics - ${componentName}`);
    Object.entries(metrics).forEach(([key, value]) => {
      console.log(`${key}:`, value);
    });
    console.groupEnd();
  }

  // In a production environment, you might send this to an analytics service
  // For now, we'll just store in a simple way
  const perfData = JSON.parse(localStorage.getItem('heroSectionPerf') || '{}');
  perfData[componentName] = { ...perfData[componentName], ...metrics, timestamp: Date.now() };
  localStorage.setItem('heroSectionPerf', JSON.stringify(perfData));
};