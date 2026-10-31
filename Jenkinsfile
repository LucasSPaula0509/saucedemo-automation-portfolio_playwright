// Pipeline opcional equivalente ao GitHub Actions (smoke -> regressão -> defeitos -> report).
// Requer: Python 3.14 no agente, Chrome/Firefox (ou os navegadores do Playwright), um JDK no PATH
// (o Allure roda na JVM) e o plugin Allure Jenkins (ferramenta "allure").
// Execução sequencial: um cenário por vez, um estágio por vez.
pipeline {
  agent any

  options {
    timestamps()
    timeout(time: 60, unit: 'MINUTES')
  }

  parameters {
    choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Navegador da regressão')
    string(name: 'TAGS', defaultValue: 'not defeito and not performance', description: 'Markers da regressão')
  }

  environment {
    CI = 'true'
  }

  stages {
    stage('Instalar') {
      steps {
        sh '''
          python3 -m venv .venv
          .venv/bin/pip install -r requirements.txt
          .venv/bin/python -m playwright install firefox
        '''
      }
    }

    // Cada estágio grava em uma pasta própria de allure-results (o --clean-alluredir limpa a pasta).
    stage('Smoke') {
      steps {
        sh '.venv/bin/pytest -m "smoke and not defeito" --alluredir=allure-results/smoke'
      }
    }

    stage('Regressão') {
      steps {
        script {
          def args = [
            chrome : '--browser chromium --browser-channel chrome',
            edge   : '--browser chromium --browser-channel msedge',
            firefox: '--browser firefox',
          ][params.BROWSER]
          sh ".venv/bin/pytest ${args} -m \"${params.TAGS}\" --alluredir=allure-results/regression"
        }
      }
    }

    stage('Defeitos conhecidos') {
      steps {
        // Falha esperada enquanto o defeito existir: marca o estágio como instável sem quebrar o build.
        catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
          sh '.venv/bin/pytest -m defeito --alluredir=allure-results/defeitos'
        }
      }
    }
  }

  post {
    always {
      allure includeProperties: false, results: [
        [path: 'allure-results/smoke'],
        [path: 'allure-results/regression'],
        [path: 'allure-results/defeitos'],
      ]
      archiveArtifacts artifacts: 'reports/**, test-results/**', allowEmptyArchive: true
    }
  }
}
